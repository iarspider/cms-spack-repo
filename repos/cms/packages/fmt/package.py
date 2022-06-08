from spack import *
from spack.pkg.builtin.fmt import Fmt as BuiltinFmt


class Fmt(BuiltinFmt):
    __doc__ = BuiltinFmt.__doc__

    def cmake_args(self):
        args = super().cmake_args()
        args.append('-DCMAKE_INSTALL_LIBDIR=lib')
        return args
