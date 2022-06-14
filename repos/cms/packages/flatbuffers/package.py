from spack import *
from spack.pkg.builtin.flatbuffers import Flatbuffers as BuiltinFlatbuffers


class Flatbuffers(BuiltinFlatbuffers):
    __doc__ = BuiltinFlatbuffers.__doc__

    def cmake_args(self):
        args = super().cmake_args()

        args.append('-DFLATBUFFERS_BUILD_CPP17=ON')
        args.append('-DFLATBUFFERS_BUILD_TESTS=OFF')
        return args
