from spack import *
from spack.pkg.builtin.dcap import Dcap as BuiltinDcap


class Dcap(BuiltinDcap):
    __doc__ = BuiltinDcap.__doc__

    drop_files = ["share", "lib/*.a"]
    strip_files = ["lib/*.so"]
