from spack import *
from spack.pkg.builtin.gmake import Gmake as BuiltinGmake


class Gmake(BuiltinGmake):
    __doc__ = BuiltinGmake.__doc__

    # -- CMS
    drop_files = ['man', 'info']
