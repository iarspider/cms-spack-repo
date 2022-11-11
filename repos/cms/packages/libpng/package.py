from spack import *
from spack.pkg.builtin.libpng import Libpng as BuiltinLibpng


class Libpng(BuiltinLibpng):
    __doc__ = BuiltinLibpng.__doc__

    # -- CMS hook
    strip_files = ["lib"]
    drop_files = ["share"]
