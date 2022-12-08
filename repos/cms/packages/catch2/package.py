from spack import *
from spack.pkg.builtin.catch2 import Catch2 as BuiltinCatch2


class Catch2(BuiltinCatch2):
    __doc__ = BuiltinCatch2.__doc__

    def cmake(self, spec, prefix):
        pass

    def build(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install("single_include/catch2/catch.hpp", prefix.include)
