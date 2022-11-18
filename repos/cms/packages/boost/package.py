import copy

from spack import *
from spack.pkg.builtin.boost import Boost as BuiltinBoost


class Boost(BuiltinBoost):
    __doc__ = BuiltinBoost.__doc__

    git = "https://github.com/cms-externals/boost.git"

    version("1.78.0.cms", commit="7f597ea02d8a714076157b4bf65fa8e5752b8468")

    depends_on("zstd")
    depends_on("xz")

    drop_patch("python_jam.patch")

    def determine_toolset(self, spec):
        if spec.satisfies("platform=darwin"):
            return "darwin"
        return super().determine_toolset(spec)

    def determine_b2_options(self, spec, options):
        threading_opts = super().determine_b2_options(spec, options)
        if "+iostreams" in spec:
            i = options.index("NO_LZMA=1")
            options.pop(i + 1)
            options.pop(i)
            i = options.index("NO_ZSTD=1")
            options.pop(i + 1)
            options.pop(i)
            options.extend(
                [
                    "-s",
                    "ZSTD_INCLUDE=%s" % spec["zstd"].prefix.include,
                    "-s",
                    "ZSTD_LIBPATH=%s" % spec["zstd"].prefix.lib,
                    "-s",
                    "LZMA_INCLUDE=%s" % spec["xz"].prefix.include,
                    "-s",
                    "LZMA_LIBPATH=%s" % spec["xz"].prefix.lib,
                ]
            )

        return threading_opts
