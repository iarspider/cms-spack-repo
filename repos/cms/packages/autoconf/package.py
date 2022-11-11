from spack import *
from spack.pkg.builtin.autoconf import Autoconf as BuiltinAutoconf


class Autoconf(BuiltinAutoconf):
    __doc__ = BuiltinAutoconf.__doc__

    # -- CMS hook
    drop_files = ["share/man", "share/doc", "share/info"]
