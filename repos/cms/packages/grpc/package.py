from spack import *
from spack.pkg.builtin.grpc import Grpc as BuiltinGrpc


class Grpc(BuiltinGrpc):
    __doc__ = BuiltinGrpc.__doc__

    version("1.35.0", sha256="27dd2fc5c9809ddcde8eb6fa1fa278a3486566dfc28335fca13eb8df8bd3b958")

    patch("grpc-ssl-fix.patch", when="^openssl")

    def cmake_args(self):
        args = super().cmake_args()
        args.extend(("-DCMAKE_CXX_STANDARD:STRING=17", "-DCMAKE_INSTALL_LIBDIR=lib"))
        return args

