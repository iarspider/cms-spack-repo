from spack import *
from spack.pkg.builtin.openmpi import Openmpi as BuiltinOpenmpi


class Openmpi(BuiltinOpenmpi):
    __doc__ = BuiltinOpenmpi.__doc__

    def configure_args(self):
        config_args = super().configure_args()
        config_args.extend(['--without-x', '--with-pic', '--with-gnu-ld', '--enable-openib-rdmacm-ibaddr'])
        return config_args
