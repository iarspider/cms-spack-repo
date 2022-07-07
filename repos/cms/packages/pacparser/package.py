from spack import *
from spack.pkg.builtin.pacparser import Pacparser as BuiltinPacparser


class Pacparser(BuiltinPacparser):
    __doc__ = BuiltinPacparser.__doc__
    parallel = False
