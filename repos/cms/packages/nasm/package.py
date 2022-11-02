from spack import *
from spack.pkg.builtin.nasm import Nasm as BuiltinNasm


class Nasm(BuiltinNasm):
    __doc__ = BuiltinNasm.__doc__

    # -- CMS hook
    drop_files = ['share']
