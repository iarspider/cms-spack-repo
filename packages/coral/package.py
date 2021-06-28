from spack import *
from glob import glob
from string import Template
import re
import fnmatch
import shutil
import sys,os

#sys.path.append(os.path.join(os.path.dirname(__file__), '../ToolfilePackage'))
#from scrampackage import relrelink, write_scram_toolfile

class Coral(ScramPackage):
    """CORAL built as a scram project"""

    homepage = "http://cms-sw.github.io"
    url = "https://github.com/cms-externals/coral.tgz"

    version('2.3.21py3', git='https://github.com/cms-externals/coral',
            branch='cms/CORAL_2_3_21py3')

    patch('coral-2_3_21-gcc8.patch')
    patch('coral-2_3_20-macosx.patch', when='platform=darwin')

    depends_on('scram')
    depends_on('gmake')
    depends_on('cmssw-config')
    depends_on('coral-tool-conf')
    depends_on('perl')

    def __init__(self, spec):
        super().__init__(spec)

        self.scram_arch = 'slc_amd64_gcc'
        if sys.platform == 'darwin':
            self.scram_arch = 'osx10_amd64_clang'

        self.cvssrc = 'coral'
        self.subpackageDebug = True

        # custom
        self.toolname = 'coral'
        self.toolconf = 'coral-tool-conf'
        # self.usercxxflags = '-fpermissive'


    def patch(self):
        if self.spec.satisfies('platform=darwin'):
            filter_file('(<classpath.*/tests\\+.*>)', '', 'config/BuildFile.xml')
            
        if self.spec.satisfies('target=aarch64:') or self.spec.satisfies('target=ppc64') or self.spec.satisfies('target=ppc64le'):
            shutil.rmtree(join_path(self.stage.source_path, 'src', 'OracleAccess'))

    def install(self, spec, prefix):
        super().install(self, prefix)
        raise RuntimeError('STOP')       

    # def install(self, spec, prefix):
        # coral_version = 'CORAL.' + str(self.version)
        # coral_u_version = coral_version.replace('.', '_')

        # scram = Executable(spec['scram'].prefix.cli+'/scram')
        # source_directory = self.stage.source_path
        # scram_version = 'V%s' % spec['scram'].version

        # config_tag = '%s' % spec['cmssw-config'].version.underscored
        # with working_dir(self.stage.path):
            # mkdirp('config')
            # install_tree(source_directory, 'src')
            # install_tree(join_path(spec['cmssw-config'].prefix), 'config')

            # with open('config/config_tag', 'w') as f:
                # f.write(config_tag+'\n' )

            # uc=Executable('config/updateConfig.py')
            # uc(  '-p', 'CORAL',
                 # '-v', '%s' % coral_u_version,
                 # '-s', '%s' % scram_version,
                 # '-t', '%s' % spec['coral-tool-conf'].prefix,
                 # '--keys', 'SCRAM_COMPILER=gcc',
                 # '--keys', 'PROJECT_GIT_HASH=' + coral_u_version)

            # scram('--arch', '%s' % self.scram_arch, 'project', '-d', os.path.realpath(self.stage.path), '-b', 'config/bootsrc.xml')

        # project_dir = os.path.realpath(join_path(self.stage.path, coral_u_version))
        # with working_dir(project_dir, create=False):
            # matches = []

            # for f in glob('src/*/*/test/BuildFile*'):
                # matches.append(f)
            # for m in matches:
                # if os.path.exists(m):
                    # os.remove(m)

            # scram.add_default_env('LOCALTOP', project_dir)
            # scram.add_default_env('CORAL_BASE', project_dir)
            # scram.add_default_env('LD_LIBRARY_PATH', '%s/lib/%s' %
                                  # (project_dir, self.scram_arch))
            # scram('build', '-v', '-j8')
            # shutil.rmtree('external')
            # shutil.rmtree('tmp')
            # os.remove('slc_amd64_gcc/python/LCG/PyCoral')
        # install_tree(project_dir, prefix+'/'+coral_u_version)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('CORAL_RELEASE_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', '%s/CORAL_%s/%s/lib' %
                              (self.prefix, self.version.underscored, self.scram_arch))

    def setup_environment(self, spack_env, run_env):
        spack_env.set('LOCALTOP', self.prefix + '/' +
                      self.version.underscored.string)
        spack_env.set('CORAL_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', '%s/CORAL_%s/%s/lib' %
                              (self.prefix, self.version.underscored, self.scram_arch))

    # @run_after('install')
    # def make_links(self):
        # with working_dir(self.spec.prefix):
            # os.symlink('CORAL_%s/include/LCG' % self.version.underscored, 'include')
            # os.symlink('CORAL_%s/%s/lib' % (self.version.underscored, self.scram_arch), 'lib')
