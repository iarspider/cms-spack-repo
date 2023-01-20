from spack import *
from spack.pkg.builtin.pythia8 import Pythia8 as BuiltinPythia8


class Pythia8(BuiltinPythia8):
    __doc__ = BuiltinPythia8.__doc__

    patch("29.diff", when="@8.306")
