import llnl.util.filesystem
from llnl.util.filesystem import * 

from spack.package import PackageBase, run_after
from spack.directives import depends_on
from spack.util.executable import which, Executable

import platform
import os
import shutil

class ScramPackage(PackageBase):
    subpackageDebug = True
    vectorized_build = None # at buildtime
    package_vectorization = ""
    cmsplatf = 'slc7_amd64'
    buildtarget = 'release-build'
    cvstag = None # at buildtime
    scram_compiler = 'gcc' # at buildtime
    usercxxflags = None
    configtag = None
    nolibchecks = False
    prebuildtarget = None
    saveDeps = False
    runGlimpse = False

    extraOptions = None
    cvssrc = None
    buildarch = None
    ucprojtype = None
    lcprojtype = None
    toolconf = None

    bootstrapfile = 'config/bootsrc.xml'

    build_system_class = 'ScramPackage'
    phases = ['edit', 'build', 'install']

    depends_on('scram', type='build')
    depends_on('cmssw-config', type='build')
    # NOTICE: maybe dwz, once I figure it out    

    @property
    def build_directory(self):
        """Returns the directory containing the main Makefile

        :return: build directory
        """
        return self.stage.source_path

    def setup(self, spec, prefix):
        """
        # TODO: figure this out.
        %if "%{?subpackageDebug:set}" == "set"
        # note: do not change the order of the -fdebug-prefix-map options, they seem to be use in reverse order
        %define extraOptions USER_CXXFLAGS='-fdebug-prefix-map=%{cmsroot}=%{installroot} -fdebug-prefix-map=%{instroot}=%{installroot} -g %{?usercxxflags}'
        %else
        %if "%{?usercxxflags:set}" == "set"
        %define extraOptions USER_CXXFLAGS='%{usercxxflags}'
        %else
        %define extraOptions %{nil}
        %endif
        %endif
        """
        self.subpackageDebug = self.subpackageDebug and (platform.system() == 'linux')
        
        if self.subpackageDebug:
            self.usercxxflags = '-g ' + (self.usercxxflags or '')

        if self.usercxxflags is not None:
            extraOptions = "USER_CXXFLAGS='%s'" % self.usercxxflags

        if self.configtag is None:
            self.configtag = 'V06-02-13'

        if self.cvssrc is None:
            self.cvssrc = __name__.replace('-patch', '').upper()

        if self.buildarch is None:
            self.buildarch = ':'

        if self.ucprojtype is None:
            self.ucprojtype = __name__.replace('-patch', '').upper()

        self.lcprojtype = self.ucprojtype.lower()
        self.toolconf = __name__.replace('-', '_').upper() + '_TOOL_CONF_ROOT'

    def edit(self, spec, prefix):
        self.setup(spec, prefix)
        config_dir = join_path(self.stage.path, 'config')
        mkdirp(config_dir)
        install_tree(spec['cmssw-config'].prefix, join_path(self.stage.path, 'config'))
        if getattr(self, 'PatchReleaseAdditionalPackages', None) is not None:
            self.PatchReleaseAdditionalPackages()

        with working_dir(self.stage.path):
            with open("config/config_tag", "w") as f:
                f.write(self.configtag+'\n')

            uc = Executable('config/bin/updateConfig.py')
            uc('-p', self.ucprojtype, '-v', str(self.spec.version),
               '-s', str(self.spec['scram'].version), '-t', '${' + self.toolconf + '}',
               '--keys', 'PROJECT_GIT_HASH=' + str(self.spec.version))

            if self.vectorized_build:
                filter_file(' SCRAM_TARGETS=.*', ' SCRAM_TARGETS="%s"' % self.package_vectorization, 'config/Self.xml')
                filter_file('</tool>', '<runtime name="SCRAM_TARGET" value="auto"/><runtime name="USER_TARGETS_ALL" value="1"/></tool>', 'config/Self.xml')

            if getattr(self, 'PartialBootstrapPatch', None):
                self.PartialBootstrapPatch()

            scram = Executable(self.spec['scram'].cli.scram)
            scram('--arch', self.cmsplatf, 'project', '-d', self.stage.path, '-b', 'config/bootsrc.xml')


    def build(self, spec, prefix):
        lines = [
                '#!/bin/bash -xe\n',
                'i=' + str(self.stage.path),
                'srctree=spack-src',
                'scramcmd=' + self.spec['scram'].cli.scram + ' --arch' + cmsplatf,
                'compileOptions=' + self.compileOptions,
                'extraOptions=' + self.extraOptions,
                'buildtarget=' + self.buildtarget,
                'cmsroot=' + self.prefix
            ]

        if getattr(self, ignore_compile_errors, None):
            lines.append('ignore_compile_errors=/bin/true')
        else:
            lines.append('ignore_compile_errors=/bin/false')

        lines.extend([
                'rm -rf `find %{i}/%{srctree} -type d -name cmt`',
                'grep -r -l -e "^#!.*perl.*" %{i}/%{srctree} | xargs perl -p -i -e "s|^#!.*perl(.*)|#!/usr/bin/env perl\$1|"',
                '${scramcmd} arch',
                'cd $i/${srctree}'])

        extra_tools_ = getattr(self, extra_tools, [])
        for t in extra_tools_:
            lines.append('$scramcmd setup ' + t)

        lines.extend(['export BUILD_LOG=yes',
                      'export SCRAM_NOPLUGINREFRESH=yes',
                      'scram b clean',
                      'if [ $(uname) = Darwin ]; then',
                      '  # %scramcmd doesn\'t know the rpath variable on darwin...',
                      '  $scramcmd b echo_null # ensure lib, bin exist',
                      '  eval `$scramcmd runtime -sh`',
                      '  export DYLD_LIBRARY_PATH=$LD_LIBRARY_PATH',
                      'fi'])

        if self.nolibchecks:
            lines.extend(['export SCRAM_NOLOADCHECK=true', 'export SCRAM_NOSYMCHECK=true'])

        if getattr(self, 'preBuildCommand', None):
            lines.extend(self.preBuildCommand)

        lines.append('$scramcmd b -r echo_CXX </dev/null')

        if getattr(self, 'PatchReleasePythonSymlinks', None):
            lines.extend(self.PatchReleasePythonSymlinks)

        if self.prebuildtarget is not None:
            lines.append('${scramcmd} b --verbose -f ' + self.prebuildtarget + ' </dev/null')

        if __name__ == 'cmssw' or __name__ == 'cmssw-patch':
            lines.append('${scramcmd} b -f -k ' + make_jobs + ' llvm-ccdb </dev/null || true')

        if self.vectorized_build:
            lines.append('touch ${i}/.SCRAM/${cmsplatf}/multi-targets')

        lines.append('$scramcmd b --verbose -f ${compileOptions} ${extraOptions} ' + make_jobs + '${buildtarget} </dev/null || { touch ../build-errors && $scramcmd b -f outputlog && [ "${?ignore_compile_errors:set}" == "set" ]; }')

        if getattr(self, 'additionalBuildTarget0', None):
            lines.append('$scramcmd b --verbose -f ' + self.additionalBuildTarget0 + ' < /dev/null')

        if getattr(self, 'postbuildtarget', None):
            lines.append('$scramcmd b --verbose -f ' + self.postbuildtarget + ' < /dev/null')

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
                          'SCRAM_TOOL_HOME=' + self.spec['scram'].prefix + ' $i/config/SCRAM/findDependencies.py -rel $i -arch $cmsplatf'])
            if getattr(self, 'PatchReleaseDependencyInfo', None):
                lines.extend(self.PatchReleaseDependencyInfo)

            lines.append('gzip -f %i/etc/dependencies/*.out')


        lines.extend(['eval `$scramcmd run -sh`',
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
                      'done'])

        with open('build.sh', 'w') as f:
            f.write('\n'.join(lines))

        bash = which('bash')
        bash('./build.sh')

    def install(self, spec, prefix):
        lines = [
            '#!/bin/bash -xe\n',
            'i=' + str(self.stage.path),
            'srctree=spack-src',
            'scramcmd=' + self.spec['scram'].cli.scram + ' --arch' + cmsplatf,
            'compileOptions=' + self.compileOptions,
            'extraOptions=' + self.extraOptions,
            'buildtarget=' + self.buildtarget,
            'cmsroot=' + self.prefix,
            'SCRAM_ARCH=$cmsplatf ; export SCRAM_ARCH',
            'cd $i',
            '$scramcmd install -f',
            'rm -rf external/$cmsplatf; SCRAM_TOOL_HOME= ' + self.spec['scram'].prefix + ' ./config/SCRAM/linkexternal.py --arch $cmsplatf'
        ]

        if getattr(self, 'PartialReleasePackageList', None):
            lines.extend(self.PartialReleasePackageList)

        if getattr(self, 'PatchReleaseSourceSymlinks', None):
            lines.extend(self.PatchReleaseSourceSymlinks)

        if self.runGlimpse:
            lines.append('$scramcmd b --verbose -f gindices </dev/null')

        if getattr(self, 'RelocatePatchReleaseSymlinks', None):
            lines.extend(self.RelocatePatchReleaseSymlinks)

        lines.append("tar czf src.tar.gz ${srctree}")
        lines.append("rm -fR %{srctree} tmp")

        if self.subpackageDebug:
            lines.append('touch $i/.SCRAM/$cmsplatf/subpackage-debug')
            if __name__ == 'coral':
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
                          '      ' + self.spec['dwz'].prefix.bin.dwz +' -m .debug/common-symbols.debug -M common-symbols.debug $ELF_BINS || true',
                          '    fi',
                          "    echo \"$ELF_BINS\" | xargs -t -n1 -P${compiling_processes} -I$ sh -c 'objcopy --compress-debug-sections --only-keep-debug $ .debug/$.debug; objcopy --strip-debug --add-gnu-debuglink=.debug/$.debug $'",
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

        lines.extend(['for L in `find external/$cmsplatf -type l`; do',
                      '  lnk=`readlink -n $L 2>&1`',
                      '  case $lnk in',
                      '     ${cmsroot}/*)',
                      "       rl=`echo $L | sed -e 's|[^/]*/|../|g;' | xargs dirname`",
                      '       al=`echo $lnk | sed -e "s|^${cmsroot}/|../../../../$rl/|"`',
                      '       rm -f $L',
                      '       ln -sf  $al $L',
                      '       ;;',
                      '   esac',
                      'done',
                      'find external/$cmsplatf -type l | xargs ls -l'])
        if getattr(self, 'PatchReleaseSymlinkRelocate', None):
            lines.extend(self.PatchReleaseSymlinkRelocate)

        lines.append('echo "${cmsroot}" > ${i}/config/scram_basedir')
        with open('build.sh', 'w') as f:
            f.write('\n'.join(lines))

        bash = which('bash')
        bash('./build.sh')

        self.post_(spec, prefix)

    def post_(self, spec, prefix):
        return
        
    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    # Check that self.prefix is there after installation
    # TODO: uncomment
    # run_after('install')(PackageBase.sanity_check_prefix)     