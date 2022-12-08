from spack import *
from spack.pkg.builtin.intel_tbb import IntelTbb as BuiltinIntelTbb


class IntelTbb(BuiltinIntelTbb):
    __doc__ = BuiltinIntelTbb.__doc__

    version(
        "2021.5.0",
        sha256="e5b57537c741400cf6134b428fc1689a649d7d38d9bb9c1b6d64f092ea28178a",
    )

    def cmake_args(self):
        args = super().cmake_args()
        args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        return args
