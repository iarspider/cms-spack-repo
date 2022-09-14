from spack import *
from glob import glob
from string import Template
import re
import fnmatch
import shutil
import sys, os


# sys.path.append(os.path.join(os.path.dirname(__file__), '../ToolfilePackage'))
# from scrampackage import relrelink, write_scram_toolfile

class Coral(ScramPackage):
    """CORAL built as a scram project"""

    homepage = "http://cms-sw.github.io"
    url = "https://github.com/cms-externals/coral.tgz"

    version('CORAL_2_3_21', git='https://github.com/cms-externals/coral',
            commit='a879b41c994fa956ff0ae78e3410bb409582ad20')

    patch('coral-2_3_21-gcc8.patch')
    patch('coral-2_3_20-macosx.patch', when='platform=darwin')

    depends_on('scram')
    depends_on('gmake')
    depends_on('coral-tool-conf')

    def __init__(self, spec):
        super().__init__(spec)

        self.cvssrc = 'coral'
        self.subpackageDebug = False

        # custom
        self.toolname = 'coral'
        self.toolconf = 'coral-tool-conf'
        self.usercxxflags = ['-fPIC', '-pthread'] # HACK

    def patch(self):
        if self.spec.satisfies('platform=darwin'):
            filter_file('(<classpath.*/tests\\+.*>)', '', 'config/BuildFile.xml')

        if self.spec.satisfies('target=aarch64:') or self.spec.satisfies('target=ppc64') or self.spec.satisfies(
                'target=ppc64le'):
            shutil.rmtree(join_path(self.stage.source_path, 'src', 'OracleAccess'))

    def install(self, spec, prefix):
        super().install(self, prefix)
        # raise RuntimeError('STOP')
        if self.spec.satisfies('platform=darwin'):
            dynamic_path_var = 'DYLD_FALLBACK_LIBRARY_PATH'
        else:
            dynamic_path_var = 'LD_LIBRARY_PATH'

        initsh = open(join_path(os.path.dirname(__file__), 'init.sh.in')).read()
        initcsh = open(join_path(os.path.dirname(__file__), 'init.csh.in')).read()

        mkdirp(join_path(prefix, 'etc', 'profile.d'))
        with open(join_path(prefix, 'etc', 'profile.d', 'init.sh'), 'w') as f:
            f.write(initsh.format(pkginstroot=prefix, dynamic_path_var=dynamic_path_var, pkgversion=str(
                self.spec.version)))

        with open(join_path(prefix, 'etc', 'profile.d', 'init.csh'), 'w') as f:
            f.write(initcsh.format(pkginstroot=prefix, dynamic_path_var=dynamic_path_var, pkgversion=str(
                self.spec.version)))

        if not os.path.exists(join_path(prefix.etc.scramrc, 'coral.map')):
            mkdirp(prefix.etc.scramrc)
            with open(join_path(prefix.etc.scramrc, 'coral.map'), 'w') as f:
                f.write('{ucprojtype}=$SCRAM_ARCH/{pkgname}/{ucprojtype}_*'.format(
                    ucprojtype=self.ucprojtype, pkgname='coral'))

    def setup_run_environment(self, spack_env):
        # spack_env.set('LOCALTOP', self.prefix + '/' +
        #               self.version.underscored.string)
        spack_env.set('CORAL_BASE', self.prefix)
        spack_env.append_path('LD_LIBRARY_PATH', '%s/%s/lib' %
                              (self.prefix,  self.cmsplatf))
        spack_env.append_path('PYTHONPATH', '%s/%s/lib' %
                              (self.prefix, self.cmsplatf))
        spack_env.append_path('PYTHONPATH', '%s/%s/python' %
                              (self.prefix, self.cmsplatf))

    def setup_build_environment(self, env):
        env.unset('PYTHONHOME')
    # @run_after('install')
    # def make_links(self):
    # with working_dir(self.spec.prefix):
    # os.symlink('CORAL_%s/include/LCG' % self.version.underscored, 'include')
    # os.symlink('CORAL_%s/%s/lib' % (self.version.underscored, self.cmsplatf), 'lib')
