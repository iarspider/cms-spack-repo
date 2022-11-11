import copy

from spack import *
from spack.pkg.builtin.gnuplot import Gnuplot as BuiltinGnuplot


class Gnuplot(BuiltinGnuplot):
    __doc__ = BuiltinGnuplot.__doc__

    drop_dependency("readline")

    def configure_args(self):
        args = [x for x in super().configure_args() if "readline" not in x]
        args.append("--without-readline")
        return args
