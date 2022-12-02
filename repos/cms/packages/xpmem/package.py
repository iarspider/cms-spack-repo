from spack import *
from spack.pkg.builtin.xpmem import Xpmem as BuiltinXpmem


class Xpmem(BuiltinXpmem):
    __doc__ = BuiltinXpmem.__doc__

    version("2.6.5-20220308", commit="61c39efdea943ac863037d7e35b236145904e64d")

    drop_files = ["etc"]

    def configure_args(self):
        args = super().configure_args()
        args.extend(
            [
                "--enable-shared",
                "--disable-static",
                "--disable-dependency-tracking",
                "--with-pic",
                "--with-gnu-ld",
            ]
        )
        return args
