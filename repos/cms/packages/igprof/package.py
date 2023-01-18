from spack import *
from spack.pkg.builtin.igprof import Igprof as BuiltinIgprof


class Igprof(BuiltinIgprof):
    __doc__ = BuiltinIgprof.__doc__
    git = "https://github.com/cms-externals/igprof.git"

    version("5.9.16.cms", commit="2cd0b7d4fb21223b273c5a085cec2963c8206056")

    @when("target=ppc64le:")
    def build(self, spec, prefix):
        return

    @when("target=ppc64le:")
    def install(self, spec, prefix):
        with open(join_path(prefix, "dummy"), "w") as f:
            f.write("## PLACEHOLDER ##")
