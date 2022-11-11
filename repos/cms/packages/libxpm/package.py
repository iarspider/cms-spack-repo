import copy

from spack import *
from spack.pkg.builtin.libxpm import Libxpm as BuiltinLibxpm


class Libxpm(BuiltinLibxpm):
    __doc__ = BuiltinLibxpm.__doc__

    drop_dependency("gettext")

    def configure_args(self):
        args = super().configure_args()
        args.append("--disable-nls")
