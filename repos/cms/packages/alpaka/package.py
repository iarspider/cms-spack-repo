from spack import *
from spack.pkg.builtin.alpaka import Alpaka as BuiltinAlpaka


class Alpaka(BuiltinAlpaka):
    __doc__ = BuiltinAlpaka.__doc__

    version("20230209", commit="d1855b1b0d0a2877b06147eacf0ddda56e40d661")
    version("20230201", commit="a68c866cc6c3019748cf127b4eac61be38e7f687")
    version("20220902", commit="b518e8c943a816eba06c3e12c0a7e1b58c8faedc")
    version("20220621", commit="5a4691c82676176fd8b71e1f57bb809f8c75a095")

    def cmake(self, spec, prefix):
        return

    def build(self, spec, prefix):
        return

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install_tree("include", prefix.include)
