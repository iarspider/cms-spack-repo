from spack import *
from spack.pkg.builtin.libxml2 import Libxml2 as BuiltinLibxml2


class Libxml2(BuiltinLibxml2):
    __doc__ = BuiltinLibxml2.__doc__

    # -- CMS hook
    drop_files = ['lib/*.la']
