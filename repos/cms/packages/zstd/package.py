from spack import *
from spack.pkg.builtin.zstd import CMakeBuilder as BuiltinZstdCMakeBuilder, MakefileBuilder as BuiltinMakefileBuilder, Zstd as BuiltinZstd

class Zstd(BuiltinZstd):
    __doc__ = BuiltinZstd.__doc__

class CMakeBuilder(BuiltinZstdCMakeBuilder):
    def cmake_args(self):
        args = super().cmake_args()
        args += [
            "-DZSTD_BUILD_CONTRIB:BOOL=OFF",
            "-DZSTD_BUILD_TESTS:BOOL=OFF",
            "-DZSTD_LEGACY_SUPPORT:BOOL=OFF",
            "-DCMAKE_INSTALL_LIBDIR:STRING=lib",
            "-Dzstd_VERSION:STRING=" + str(self.spec.version),
        ]

        return args

class MakefileBuilder(BuiltinMakefileBuilder):
    pass
