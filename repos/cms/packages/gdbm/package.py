import copy

from spack import *
from spack.pkg.builtin.gdbm import Gdbm as BuiltinGdbm


class Gdbm(BuiltinGdbm):
    __doc__ = BuiltinGdbm.__doc__

    def configure_args(self):
        args = super().configure_args()
        args.append("--disable-nls")
        return args
