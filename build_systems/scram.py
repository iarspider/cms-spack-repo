from llnl.util.filesystem import *

from spack.package import PackageBase, run_after
from spack.directives import depends_on, resource
from spack.util.executable import which, Executable

import platform
import os
import shutil


class ScramPackage(PackageBase):
    phases = ['edit', 'build', 'install']

    depends_on('scram', type='build')
    depends_on('dwz', type='build')

    configtag = 'V07-00-06'

    resource(name='cmssw-config', git='https://github.com/cms-sw/cmssw-config.git',
             tag='V07-00-06')

    def __init__(self, spec):
        super().__init__(spec)
        self.toolname = ''
        self.subpackageDebug = True
        self.vectorized_build = False  # at buildtime
        self.package_vectorization = ""
        self.cmsplatf = os.environ['SCRAM_ARCH']
        self.buildtarget = 'release-build'
        self.cvstag = None  # at buildtime
        self.scram_compiler = 'gcc'  # at buildtime
        self.usercxxflags = ''
        self.configtag = None
        self.nolibchecks = False
        self.prebuildtarget = None
        self.saveDeps = False
        self.runGlimpse = False
        self.ignore_compile_errors = False

        self.extraOptions = ''
        self.cvssrc = None
        self.buildarch = None
        self.ucprojtype = None
        self.lcprojtype = None
        self.toolconf = None

        self.bootstrapfile = 'config/bootsrc.xml'

        self.build_system_class = 'ScramPackage'



    @property
    def build_directory(self):
        """Returns the directory containing the main Makefile

        :return: build directory
        """
        return self.stage.source_path

    def setup_build_environment(self, env):
        if isinstance(self.usercxxflags, str):
            self.usercxxflags = [self.usercxxflags]
        for flag in self.usercxxflags:
            env.append_flags('USER_CXXFLAGS', flag)

        self.subpackageDebug = self.subpackageDebug and (platform.system() == 'linux')

        if self.subpackageDebug:
            # HACK: hardcoded `/opt/cmssw`
            debugflags = '-fdebug-prefix-map={0}={1} -fdebug-prefix-map={2}={1} -g'.format(str(self.stage.path),
                                                                                           '/opt/cmssw',
                                                                                           str(self.prefix))
            debugflags = debugflags.split(' ')
        else:
            debugflags = []

        for flag in debugflags:
            env.append_flags('USER_CXXFLAGS', flag)

    def setup(self, spec, prefix):
        """
        """

        #if self.usercxxflags is not None:
        #    self.extraOptions = "USER_CXXFLAGS='%s'" % (self.usercxxflags + debugflags)

        if self.configtag is None:
            self.configtag = 'V07-06-00'

        if self.cvssrc is None:
            self.cvssrc = self.toolname.replace('-patch', '').upper()

        if self.ucprojtype is None:
            self.ucprojtype = self.toolname.replace('-patch', '').upper()

        self.lcprojtype = self.ucprojtype.lower()

        if getattr(self, 'toolconf', None) is None:
            self.toolconf = self.toolname.replace('-', '_').upper() + '-tool-conf'

    def edit(self, spec, prefix):
        bash = which('bash')

        self.setup(spec, prefix)
        config_dir = join_path(self.stage.path, 'config')
        mkdirp(config_dir)
        os.rename(self.stage.source_path, join_path(self.stage.path, 'src'))
        os.rename(self.stage[1].source_path, config_dir)
        self.srctree = 'src'

        if getattr(self, 'PatchReleaseAdditionalPackages', None) is not None:
            with open('edit_PatchReleaseAdditionalPackages.sh', 'w') as f:
                f.write('#!/bin/bash\n')
                f.write('\n'.join(self.PatchReleaseAdditionalPackages))

            bash('-xe', './edit_PatchReleaseAdditionalPackages.sh')

        with working_dir(self.stage.path):
            with open("config/config_tag", "w") as f:
                f.write(self.configtag + '\n')

            uc = Executable('config/updateConfig.py')
            uc('-p', self.ucprojtype, '-v', str(self.spec.version),
               '-s', str(self.spec['scram'].version), '-t', self.spec[self.toolconf].prefix,
               '--keys', 'PROJECT_GIT_HASH=' + str(self.spec.version))

            if self.vectorized_build:
                filter_file(' SCRAM_TARGETS=.*', ' SCRAM_TARGETS="%s"' % self.package_vectorization, 'config/Self.xml')
                filter_file('</tool>',
                            '<runtime name="SCRAM_TARGET" value="auto"/><runtime name="USER_TARGETS_ALL" '
                            'value="1"/></tool>',
                            'config/Self.xml')

            if getattr(self, 'release_usercxxflags', None):
                with open("config/BuildFile.xml", "a") as f:
                    f.write('<flags CXXFLAGS="' + self.release_usercxxflags + '"/>\n')

            if getattr(self, 'PartialBootstrapPatch', None):
                with working_dir(self.stage.path):
                    with open('edit_PartialBootstrapPatch.sh', 'w') as f:
                        f.write('#!/bin/bash\n')
                        f.write('\n'.join(self.PartialBootstrapPatch))

                    bash = which('bash')
                    bash('-xe', './edit_PartialBootstrapPatch.sh')

            scram = which('scram')
            scram('--arch', self.cmsplatf, 'project', '-d', self.stage.path, '-b', 'config/bootsrc.xml')

    def build(self, spec, prefix):
        scramcmd = self.spec['scram'].prefix.bin.scram + ' --arch ' + self.cmsplatf
        lines = [
            '#!/bin/bash -xe',
            'i=' + join_path(self.stage.path, str(spec.version)),
            'srctree=' + self.srctree,
            'compileOptions=' + ('-k' if self.ignore_compile_errors else ''),
            'extraOptions=' + self.extraOptions,
            'buildtarget=' + self.buildtarget,
            'cmsroot=' + self.stage.path,
            '#cd ' + join_path(self.stage.path, self.srctree),
            'export SCRAM_DEBUG=1'
        ]

        if self.ignore_compile_errors:
            lines.append('ignore_compile_errors=/bin/true')
        else:
            lines.append('ignore_compile_errors=/bin/false')

        lines.extend([
            'rm -rf `find $i/$srctree -type d -name cmt`',
            'grep -r -l -e "^#!.*perl.*" ${i}/${srctree} | xargs perl -p -i -e "s|^#!.*perl(.*)|#!/usr/bin/env '
            r'perl\$1|"',
            scramcmd + ' arch',
            'cd ${i}/${srctree}'])

        extra_tools_ = getattr(self, 'extra_tools', [])
        for t in extra_tools_:
            lines.append(scramcmd + ' setup ' + t)

        lines.extend(['export BUILD_LOG=yes',
                      'export SCRAM_NOPLUGINREFRESH=yes',
                      scramcmd + ' b clean',
                      'if [ $(uname) = Darwin ]; then',
                      '  # %scramcmd doesn\'t know the rpath variable on darwin...',
                      '  ' + scramcmd + ' b echo_null # ensure lib, bin exist',
                      '  eval `' + scramcmd + ' runtime -sh`',
                      '  export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH',
                      'fi'])

        if self.nolibchecks:
            lines.extend(['export SCRAM_NOLOADCHECK=true', 'export SCRAM_NOSYMCHECK=true'])

        if getattr(self, 'preBuildCommand', None):
            lines.extend(self.preBuildCommand)

        lines.append(scramcmd + ' b -r echo_CXX </dev/null')

        if getattr(self, 'PatchReleasePythonSymlinks', None):
            lines.extend(self.PatchReleasePythonSymlinks)

        if self.prebuildtarget is not None:
            lines.append(scramcmd + ' b --verbose -f ' + self.prebuildtarget + ' </dev/null')

        if self.toolname == 'cmssw' or self.toolname == 'cmssw-patch':
            lines.append(scramcmd + ' b -f -k -j' + str(make_jobs) + ' llvm-ccdb </dev/null || true')

        if self.vectorized_build:
            lines.append('touch ${i}/.SCRAM/${cmsplatf}/multi-targets')

        lines.append(scramcmd + ' b --verbose -f ${compileOptions} ${extraOptions} -j' + str(
            make_jobs) + ' ${buildtarget} </dev/null || { touch ../build-errors && ' + scramcmd + ' b -f outputlog && '
                                                                                                  '/bin/' + str(
            self.ignore_compile_errors).lower() + ' ; }')

        if getattr(self, 'additionalBuildTarget0', None):
            lines.append(scramcmd + ' b --verbose -f ' + self.additionalBuildTarget0 + ' < /dev/null')

        if getattr(self, 'postbuildtarget', None):
            lines.append(scramcmd + ' b --verbose -f ' + self.postbuildtarget + ' < /dev/null')

        # Move the debug logs into the builddir, so that they do not get packaged.
        lines.extend(['LOG_WEB_DIR=$cmsroot/WEB/build-logs/${cmsplatf}/${v}',
                      'rm -rf ${LOG_WEB_DIR}',
                      'mkdir -p ${LOG_WEB_DIR}/logs/src',
                      'if [ -d ${i}/tmp/${cmsplatf}/cache/log/src ]; then',
                      '  pushd ${i}/tmp/${cmsplatf}/cache/log/src',
                      '    tar czf ${LOG_WEB_DIR}/logs/src/src-logs.tgz ./',
                      '  popd',
                      'fi'
                      ])

        if self.saveDeps:
            lines.extend(['mkdir -p $i/etc/dependencies',
                          'SCRAM_TOOL_HOME=' + self.spec[
                              'scram'].prefix + ' $i/config/SCRAM/findDependencies.py -rel $i -arch $cmsplatf'])
            if getattr(self, 'PatchReleaseDependencyInfo', None):
                lines.extend(self.PatchReleaseDependencyInfo)

            lines.append('gzip -f $i/etc/dependencies/*.out')

        lines.extend(['eval `' + scramcmd + ' run -sh`',
                      'for cmd in edmPluginRefresh ; do',
                      '  cmdpath=`which $cmd 2> /dev/null || echo ""`',
                      '  if [ "X$cmdpath" != X ] ; then',
                      '    for lib in ${cmssw_libs} ; do',
                      '      if [ -d $i/$lib ] ; then',
                      '        rm -f $i/$lib/.edmplugincache',
                      '        $cmd $i/$lib || true',
                      '      fi',
                      '    done',
                      '  fi',
                      'done',
                      '',
                      'rm -rf ' + join_path(self.stage.path, str(self.spec.version), 'tmp')])

        with open('build.sh', 'w') as f:
            f.write('\n'.join(lines))

        bash = which('bash')
        bash('-xe', './build.sh')

    def install(self, spec, prefix):
        scramcmd = self.spec['scram'].prefix.bin.scram + ' --arch ' + self.cmsplatf

        lines = [
            '#!/bin/bash -xe',
            'i=' + join_path(self.stage.path, str(spec.version)),
            '_builddir=$i',
            'srctree=' + self.srctree,
            'compileOptions=' + ('-k' if self.ignore_compile_errors else ''),
            'extraOptions=' + self.extraOptions,
            'buildtarget=' + self.buildtarget,
            'cmsroot=' + prefix,
            'cmsplatf=' + self.cmsplatf,
            'SCRAM_ARCH=$cmsplatf ; export SCRAM_ARCH',
            'cd $i',
            scramcmd + ' install -f',
            'rm -rf external/$cmsplatf; SCRAM_TOOL_HOME=' + self.spec[
                'scram'].prefix + ' ./config/SCRAM/linkexternal.py --arch $cmsplatf'
        ]

        if getattr(self, 'PartialReleasePackageList', None):
            lines.extend(self.PartialReleasePackageList)

        if getattr(self, 'PatchReleaseSourceSymlinks', None):
            lines.extend(self.PatchReleaseSourceSymlinks)

        if self.runGlimpse:
            lines.append(scramcmd + ' b --verbose -f gindices </dev/null')

        if getattr(self, 'RelocatePatchReleaseSymlinks', None):
            lines.extend(self.RelocatePatchReleaseSymlinks)

        lines.append("rm -fR tmp")

        if self.subpackageDebug:
            lines.append('touch $i/.SCRAM/$cmsplatf/subpackage-debug')
            if self.toolname == 'coral':
                lines.append('ELF_DIRS="$i/$cmsplatf/lib $i/$cmsplatf/tests/bin"')
                lines.append('DROP_SYMBOLS_DIRS=""')
            else:
                lines.append('ELF_DIRS="$i/lib/$cmsplatf $i/biglib/$cmsplatf $i/bin/$cmsplatf $i/test/$cmsplatf"')
                lines.append('DROP_SYMBOLS_DIRS="$i/objs/$cmsplatf"')

            lines.extend(['for DIR in $ELF_DIRS $DROP_SYMBOLS_DIRS; do',
                          '  pushd $DIR',
                          '  mkdir -p .debug',
                          '  # ELF binaries',
                          "  ELF_BINS=$(file * | grep ELF | cut -d':' -f1)",
                          '  if [ ! -z "$ELF_BINS" ]; then',
                          '    if [ $(echo $ELF_BINS | wc -w) -gt 1 ] ; then',
                          '      dwz -m .debug/common-symbols.debug -M common-symbols.debug '
                          '$ELF_BINS || true',
                          '    fi',
                          "    echo \"$ELF_BINS\" | xargs -t -n1 -P${compiling_processes} -I$ sh -c 'objcopy "
                          "--compress-debug-sections --only-keep-debug $ .debug/$.debug; objcopy --strip-debug "
                          "--add-gnu-debuglink=.debug/$.debug $'",
                          '  fi',
                          '  popd',
                          'done',
                          '',
                          'for DIR in $DROP_SYMBOLS_DIRS; do',
                          '  rm -rf $DIR/.debug',
                          'done',
                          '',
                          '# split the debug symbols out of the main binaries, into separate files',
                          'rm -f $_builddir/files.debug $_builddir/files',
                          'touch $_builddir/files.debug $_builddir/files',
                          'for DIR in $ELF_DIRS; do',
                          "  DIR=`echo $DIR | sed 's|^$i/|${installroot}/${pkgrel}/|'`",
                          '  echo "$exclude $DIR/.debug"   >> $_builddir/files',
                          '  echo "$DIR/.debug"            >> $_builddir/files.debug',
                          'done',
                          ''])

        # Done by spack, as far as I can tell
        # lines.extend(['for L in `find external/$cmsplatf -type l`; do',
        #               '  lnk=`readlink -n $L 2>&1`',
        #               '  case $lnk in',
        #               '     ${cmsroot}/*)',
        #               "       rl=`echo $L | sed -e 's|[^/]*/|../|g;' | xargs dirname`",
        #               '       al=`echo $lnk | sed -e "s|^${cmsroot}/|../../../../$rl/|"`',
        #               '       rm -f $L',
        #               '       ln -sf  $al $L',
        #               '       ;;',
        #               '   esac',
        #               'done',
        #               'find external/$cmsplatf -type l | xargs ls -l'])
        if getattr(self, 'PatchReleaseSymlinkRelocate', None):
            lines.extend(self.PatchReleaseSymlinkRelocate)

        lines.append('echo "${cmsroot}" > ${i}/config/scram_basedir')
        with open('install.sh', 'w') as f:
            f.write('\n'.join(lines))

        bash = which('bash')
        bash('-xe', './install.sh')

        self.post_(spec, prefix)
        with working_dir(join_path(self.stage.path, str(spec.version))):
            install_tree('.', prefix, )
#        for _ in os.listdir(join_path(self.stage.path, str(spec.version))):
#            if os.path.isdir(_):
#                install_tree(join_path(self.stage.path, str(spec.version), _), prefix)
#            else:
#                install(join_path(self.stage.path, str(spec.version), _), prefix)

        # install_tree(join_path(self.stage.path, 'src'), prefix) # No idea why...

    def post_(self, spec, prefix):
        # %post part of scram-project-build.file; probably not needed for spack
        python = which('python')
        python(join_path(self.stage.path, 'config', 'SCRAM', 'projectAreaRename.py'), self.stage.path, prefix, self.cmsplatf, join_path(self.stage.path, str(self.spec.version)) )
        return

    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
