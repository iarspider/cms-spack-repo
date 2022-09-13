from spack import *
from spack.pkg.builtin.xrootd import Xrootd as BuiltinXrootd


class Xrootd(BuiltinXrootd):
    __doc__ = BuiltinXrootd.__doc__
    git = 'https://github.com/xrootd/xrootd.git'

    version('5.4.2.cms.1', commit='18210b01c0fafa807484ab821bec1d54116b1137')

    strip_files = ['lib']

    depends_on('davix', type=('build', 'run'))

    def setup_build_environment(self, env):
        # hack
        env.set('USER_VERSION', str(self.spec.version).replace('.cms', ''))

    def patch(self):
        super().patch()
        filter_file('UUID REQUIRED', 'UUID ', 'cmake/XRootDFindLibs.cmake')

    def cmake_args(self):
        args = super().cmake_args()
        args.append('-DFORCE_ENABLED=TRUE')
        args.append('-DENABLE_VOMS=FALSE')
        args.append('-DXRDCL_ONLY=TRUE')
        args.append('-DENABLE_FUSE=FALSE')
        args.append('-DENABLE_CRYPTO=TRUE')
        args.append('-DCMAKE_PREFIX_PATH=' + self.spec['davix'].prefix)
        return args
