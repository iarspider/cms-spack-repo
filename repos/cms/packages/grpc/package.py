from spack import *
from spack.pkg.builtin.grpc import Grpc as BuiltinGrpc


class Grpc(BuiltinGrpc):
    __doc__ = BuiltinGrpc.__doc__

    def cmake_args(self):
        args = super().cmake_args()
        args.append('-DCMAKE_INSTALL_LIBDIR=lib')
        return args
