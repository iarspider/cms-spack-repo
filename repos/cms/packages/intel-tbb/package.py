from spack import *
from spack.pkg.builtin.intel_tbb import IntelTbb as BuiltinIntelTbb


class IntelTbb(BuiltinIntelTbb):
    __doc__ = BuiltinIntelTbb.__doc__

    version("2021.8.0-rc1", sha256="4ee1bc8e0baed84ee189987d81d51f89f52692cadb5472c1bdabc12097f78d31")

    version(
        "2021.5.0",
        sha256="e5b57537c741400cf6134b428fc1689a649d7d38d9bb9c1b6d64f092ea28178a",
    )

    def cmake_args(self):
        args = super().cmake_args()
        new_args = []
        for arg in args:
            if arg.startswith("-DCMAKE_HWLOC_2_I") or arg.startswith("-DCMAKE_HWLOC_2_L"):
                arg = arg.replace("CMAKE_HWLOC_2", "CMAKE_HWLOC_2_5")
            new_args.append(arg)
        new_args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        return new_args
