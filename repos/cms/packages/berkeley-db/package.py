from spack import *
from spack.pkg.builtin.berkeley_db import BerkeleyDb as BuiltinBerkeleyDb


class BerkeleyDb(BuiltinBerkeleyDb):
    __doc__ = BuiltinBerkeleyDb.__doc__

    # -- CMS hook
    strip_files = 'lib'
