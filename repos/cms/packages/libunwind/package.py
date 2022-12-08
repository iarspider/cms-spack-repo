from spack import *
from spack.pkg.builtin.libunwind import Libunwind as BuiltinLibunwind


class Libunwind(BuiltinLibunwind):
    __doc__ = BuiltinLibunwind.__doc__

    version("1.6.2-master.0", commit="7cf6e84bb86ff5840896b4910ccc3865d4f00ffb")

    depends_on("autoconf", type="build", when="@1.6.2-master.0")
    depends_on("automake", type="build", when="@1.6.2-master.0")
    depends_on("libtool", type="build", when="@1.6.2-master.0")
