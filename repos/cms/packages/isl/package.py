from spack import *
from spack.pkg.builtin.isl import Isl as BuiltinIsl


class Isl(BuiltinIsl):
    __doc__ = BuiltinIsl.__doc__

    def configure_args(self):
        args = super().configure_args()
        args.append("--disable-static")
        return args
