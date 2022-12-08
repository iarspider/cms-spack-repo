from spack import *
from spack.pkg.builtin.elfutils import Elfutils as BuiltinElfutils


class Elfutils(BuiltinElfutils):
    __doc__ = BuiltinElfutils.__doc__

    def configure_args(self):
        args = super().configure_args()
        args.extend(["--enable-libdebuginfod=dummy", "--program-prefix='eu-'", "--disable-silent-rules"])

        return args
