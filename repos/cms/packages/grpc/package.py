from spack import *
from spack.pkg.builtin.grpc import Grpc as BuiltinGrpc


class Grpc(BuiltinGrpc):
    __doc__ = BuiltinGrpc.__doc__

    patch('grpc-ssl-fix.patch', when='^openssl')

    def cmake_args(self):
        args = super().cmake_args()
        args.extend(('-DCMAKE_CXX_STANDARD:STRING=17', '-DCMAKE_INSTALL_LIBDIR=lib'))
        return args

