from spack import *
from spack.pkg.builtin.vdt import Vdt as BuiltinVdt


class Vdt(BuiltinVdt):
    __doc__ = BuiltinVdt.__doc__

    keep_archives = True
