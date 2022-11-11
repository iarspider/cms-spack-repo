from spack import *
from spack.pkg.builtin.nlohmann_json import NlohmannJson as BuiltinNlohmannJson


class NlohmannJson(BuiltinNlohmannJson):
    __doc__ = BuiltinNlohmannJson.__doc__

    def cmake(self, spec, prefix):
        return

    def build(self, spec, prefix):
        return

    def install(self, spec, prefix):
        mkdirp(prefix.include.nlohmann)
        install("include/nlohmann/json_fwd.hpp", prefix.include.nlohmann)
        install("single_include/nlohmann/json.hpp", prefix.include.nlohmann)
