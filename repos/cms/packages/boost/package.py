from spack import *
from spack.pkg.builtin.boost import Boost as BuiltinBoost


class Boost(BuiltinBoost):
    __doc__ = BuiltinBoost.__doc__

    git = "https://github.com/cms-externals/boost.git"

    version("1.80.0.cms", commit="eb41967202089ab5a6e8d2f2ebf2917a36f8f872")
    version("1.78.0.cms", commit="7f597ea02d8a714076157b4bf65fa8e5752b8468")

    drop_patch("python_jam.patch")

    def determine_toolset(self, spec):
        if spec.satisfies("platform=darwin"):
            return "darwin"
        return super().determine_toolset(spec)
