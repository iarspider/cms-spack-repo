from spack import *
from spack.pkg.builtin.intel_tbb import IntelTbb as BuiltinIntelTbb


class IntelTbb(BuiltinIntelTbb):
    __doc__ = BuiltinIntelTbb.__doc__

    def cmake_args(self):
        args = super().cmake_args()
        args.append('-DCMAKE_INSTALL_LIBDIR=lib')
        return args
