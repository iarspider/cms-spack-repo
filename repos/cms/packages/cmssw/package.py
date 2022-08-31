from spack import *
from glob import glob
from string import Template
import re
import fnmatch
import shutil
from spack.util.executable import Executable
# import sys,os
# sys.path.append(os.path.join(os.path.dirname(__file__), '../ToolfilePackage'))
# from scrampackage import relrelink

class Cmssw(ScramPackage):
    """CMSSW built as a scram project"""

    homepage = "http://cms-sw.github.io"
    url = "https://github.com/cms-sw/cmssw/archive/CMSSW_10_2_0.tar.gz"
    git = 'https://github.com/cms-sw/cmssw.git'

    # variant('queue', default='', values=('', 'COVERAGE', 'EXPERIMENTAL', 'DBG', 'CMSDEPRECATED', 'FORTIFIED', 'UBSAN', 'ICC', 'CLANG', 'CXXMODULE'))

    version('CMSSW_12_5_0_pre4', tag='CMSSW_12_5_0_pre4')
    version('CMSSW_12_4_0_pre3', tag='CMSSW_12_4_0_pre3')

    depends_on('scram')
    depends_on('cmssw-tool-conf')
    depends_on('gmake')
    depends_on('llvm')
    # depends_on('mpfr', when='@12.0.0_ICC_X')
    # depends_on('icc', when='@12.0.0_ICC_X') TODO

    # if sys.platform == 'darwin':
        # patch('macos.patch')
    # else:
        # patch('linux.patch')

    # scram_arch = 'slc_amd64_gcc'
    # if sys.platform == 'darwin':
        # scram_arch = 'osx10_amd64_clang'
    def __init__(self, spec):
        super().__init__(spec)

        self.toolname = 'cmssw'
        self.toolconf = 'cmssw-tool-conf'
        self.ignore_compile_errors = False

    def edit(self, spec, prefix):
        if '_COVERAGE_X' in str(spec.version):
            self.release_usercxxflags = '-fprofile-arcs -ftest-coverage'
        if '_EXPERIMENTAL_X' in str(spec.version):
            self.release_usercxxflags = '-O3 -ffast-math -freciprocal-math -fipa-pta'
        if '_DBG_X' in str(spec.version):
            if self.spec.satisfies('arch=ppc64le'):
                self.usercxxflags = '-g'
            else:
                self.release_usercxxflags = '-g -O3 -DEDM_ML_DEBUG'
        if '_CMSDEPRECATED_X' in str(spec.version):
            self.release_usercxxflags = '-DUSE_CMS_DEPRECATED'
        if '_FORTIFIED_X' in str(spec.version):
            self.release_usercxxflags = '-fexceptions -fstack-protector-all --param=ssp-buffer-size=4 -Wp,-D_FORTIFY_SOURCE=2'
        if '_UBSAN_X' in str(spec.version):
            self.release_usercxxflags = '-g'

        super().edit(spec, prefix)

        if '_UBSAN_X' in str(spec.version):
            filter_file('</tool>', 'runtime name="UBSAN_OPTIONS" value="print_stacktrace=1"/>\n</tool>', 'config/Self.xml')

        if '_ICC_X' in str(spec.version):
            self.scram_compiler = 'icc'

        if '_CLANG_X' in str(spec.version):
            self.scram_compiler = 'llvm'
            self.extra_tools = 'llvm-cxxcompiler llvm-f77compiler llvm-ccompiler'

        if '_CXXMODULE_X' in str(spec.version):
            shutil.copy(join_path(os.path.dirname(__file__), 'CXXModules.mk'), 'config/SCRAM/GMake/CXXModules.mk')

    @run_after('install')
    def cleanup_extra_data_dirs(self):
        for dirname in glob(join_path(self.spec.prefix, 'external', self.cmsplatf, 'data?*')):
            shutil.rmtree(dirname)

    def old_setup_dependent_environment(self, spack_env, run_env, dspec):
        cmssw_version = 'CMSSW.' + str(self.version)
        cmssw_u_version = cmssw_version.replace('.', '_')
#        spack_env.set('LOCALTOP', self.prefix + '/' + cmssw_u_version)
#        spack_env.set('RELEASETOP', self.prefix + '/' + cmssw_u_version)
#        spack_env.set('CMSSW_RELEASE_BASE', self.prefix)
#        spack_env.set('CMSSW_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', self.prefix +
                              '/' + cmssw_u_version + '/lib/' + self.scram_arch)
        spack_env.append_path(
            'LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib64)

    def old_setup_environment(self, spack_env, run_env):
        cmssw_version = 'CMSSW.' + str(self.version)
        cmssw_u_version = cmssw_version.replace('.', '_')
        project_dir = join_path(os.path.realpath(self.stage.path), cmssw_u_version)
#        spack_env.set('LOCALTOP', project_dir)
#        spack_env.set('CMSSW_BASE',project_dir)
        spack_env.append_path('LD_LIBRARY_PATH',
                              project_dir + '/lib/' + self.scram_arch)
        spack_env.append_path('LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib)
        spack_env.append_path(
            'LD_LIBRARY_PATH', self.spec['llvm'].prefix.lib64)

#    @run_after('install')
#    def my_abort(self):
#        raise InstallError('!! ABORTED !!')
