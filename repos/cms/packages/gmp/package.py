from spack import *
from spack.pkg.builtin.gmp import Gmp as BuiltinGmp


class Gmp(BuiltinGmp):
    __doc__ = BuiltinGmp.__doc__

    keep_archives = True
