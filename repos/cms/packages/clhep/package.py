from spack import *
from spack.pkg.builtin.clhep import Clhep as BuiltinClhep


class Clhep(BuiltinClhep):
    __doc__ = BuiltinClhep.__doc__

    git = "https://github.com/cms-externals/clhep.git"

    version("2.4.5.1.cms", commit="f256fe37039681f7856f0e324ccf9337cdc35b51")

