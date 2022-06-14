from spack import *
from spack.pkg.builtin.dcap import Dcap as BuiltinDcap


class Dcap(BuiltinDcap):
    __doc__ = BuiltinDcap.__doc__

    # -- CMS hook
    strip_files = ['lib']
    drop_files = ['share']
