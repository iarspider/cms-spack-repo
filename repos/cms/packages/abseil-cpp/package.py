from spack import *
from spack.pkg.builtin.abseil_cpp import AbseilCpp as BuiltinAbseilCpp


class AbseilCpp(BuiltinAbseilCpp):
    __doc__ = BuiltinAbseilCpp.__doc__

    strip_files = "lib"
    patch("arm.patch")

    def cmake_args(self):
        args = super().cmake_args()
        args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        return args
