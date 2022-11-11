from spack import *
from spack.pkg.builtin.expat import Expat as BuiltinExpat


class Expat(BuiltinExpat):
    __doc__ = BuiltinExpat.__doc__

    # -- CMS hook
    drop_files = ["share"]
