from spack import *
from spack.pkg.builtin.libunwind import Libunwind as BuiltinLibunwind


class Libunwind(BuiltinLibunwind):
    __doc__ = BuiltinLibunwind.__doc__

    version('1.6.2-master.0', commit='7cf6e84bb86ff5840896b4910ccc3865d4f00ffb')
