from spack import *
from spack.pkg.builtin.libffi import Libffi as BuiltinLibffi


class Libffi(BuiltinLibffi):
    __doc__ = BuiltinLibffi.__doc__

    drop_files = ['share']
