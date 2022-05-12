from spack import *
from spack.pkg.builtin.xrootd import Xrootd as BuiltinXrootd


class Xrootd(BuiltinXrootd):
    __doc__ = BuiltinXrootd.__doc__
    git = 'https://github.com/xrootd/xrootd.git'

    version('5.4.2', commit='332967cdc6553aebff0fd356254d4cdab9c9e515')

    strip_files = ['lib']
