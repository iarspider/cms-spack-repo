from spack import *
from spack.pkg.builtin.xrootd import Xrootd as BuiltinXrootd


class Xrootd(BuiltinXrootd):
    __doc__ = BuiltinXrootd.__doc__
    git = 'https://github.com/xrootd/xrootd.git'

    version('5.4.2.cms.1', commit='18210b01c0fafa807484ab821bec1d54116b1137')

    strip_files = ['lib']

    depends_on('davix', type=('build', 'run'))

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
        # drop extra parts from the version; 'v' is REQUIRED
        # see https://github.com/xrootd/xrootd/blob/v5.5.0/genversion.sh#L7
        args.append('-DUSER_VERSION=v' + str(self.spec.version[:3].dotted))
        return args
