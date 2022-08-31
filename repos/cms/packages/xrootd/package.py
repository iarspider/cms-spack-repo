from spack import *
from spack.pkg.builtin.xrootd import Xrootd as BuiltinXrootd


class Xrootd(BuiltinXrootd):
    __doc__ = BuiltinXrootd.__doc__
    git = 'https://github.com/xrootd/xrootd.git'

    version('5.4.2.cms', commit='332967cdc6553aebff0fd356254d4cdab9c9e515')

    strip_files = ['lib']

    def setup_build_environment(self, env):
        # hack
        env.set('USER_VERSION', 'v'+str(self.spec.version).replace('.cms', ''))

    def patch(self):
        super().patch()
        filter_file('UUID REQUIRED', 'UUID ', 'cmake/XRootDFindLibs.cmake')

    def cmake_args(self):
        args = super().cmake_args()
        args.append('-DFORCE_ENABLED=TRUE')
        args.append('-DENABLE_VOMS=FALSE')
        args.append('-DXRDCL_ONLY=TRUE')
        return args
