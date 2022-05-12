from spack import *
from spack.pkg.builtin.mpfr import Mpfr as BuiltinMpfr


class Mpfr(BuiltinMpfr):
    __doc__ = BuiltinMpfr.__doc__

    keep_archives = True
