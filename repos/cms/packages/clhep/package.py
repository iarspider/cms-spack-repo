from spack import *
from spack.pkg.builtin.clhep import Clhep as BuiltinClhep


class Clhep(BuiltinClhep):
    __doc__ = BuiltinClhep.__doc__

    def patch(self):
        return

    @property
    def root_cmakelists_dir(self):
        return self.stage.source_path
