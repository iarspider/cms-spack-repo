from spack import *
from spack.pkg.builtin.alpaka import Alpaka as BuiltinAlpaka


class Alpaka(BuiltinAlpaka):
    __doc__ = BuiltinAlpaka.__doc__

    version('20220621', commit='5a4691c82676176fd8b71e1f57bb809f8c75a095')

    def cmake(self, spec, prefix):
        return

    def build(self, spec, prefix):
        return

    def install(self, spec, prefix):
        install_tree('include', prefix)
