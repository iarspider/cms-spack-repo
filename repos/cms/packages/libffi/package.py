from spack import *
from spack.pkg.builtin.libffi import Libffi as BuiltinLibffi


class Libffi(BuiltinLibffi):
    __doc__ = BuiltinLibffi.__doc__

    drop_files = ["share"]

    def configure_args(self):
        args = super().configure_args()
        args.extend(("--enable-portable-binary", "--disable-static", "--disable-dependency-tracking", "--disable-docs"))
        return args
