import copy

from spack import *
from spack.pkg.builtin.sherpa import Sherpa as BuiltinSherpa


class Sherpa(BuiltinSherpa):
    __doc__ = BuiltinSherpa.__doc__

    def patch(self):
        super().patch()

        # CMS: avoid makeinfo dependency
        filter_file("Manual", "# Manual", "Makefile.am")
