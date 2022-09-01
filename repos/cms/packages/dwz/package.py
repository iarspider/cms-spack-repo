from spack import *
from spack.pkg.builtin.dwz import Dwz as BuiltinDwz


class Dwz(BuiltinDwz):
    __doc__ = BuiltinDwz.__doc__

    version('0.14-20220401', commit='b612e38de2a1a376362cc2ac0da3c0938b8e0bca')
