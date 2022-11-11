from spack import *
from spack.pkg.builtin.re2 import Re2 as BuiltinRe2


class Re2(BuiltinRe2):
    __doc__ = BuiltinRe2.__doc__

    def cmake_args(self):
        args = super().cmake_args()
        args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        return args
