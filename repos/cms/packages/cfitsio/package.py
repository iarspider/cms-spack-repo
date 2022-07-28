from spack import *
from spack.pkg.builtin.cfitsio import Cfitsio as BuiltinCfitsio


class Cfitsio(BuiltinCfitsio):
    __doc__ = BuiltinCfitsio.__doc__

    def configure_args(self):
        args = super().configure_args()
        args.extend(('--enable-reentrant', '--enable-sse2'))
        return args
