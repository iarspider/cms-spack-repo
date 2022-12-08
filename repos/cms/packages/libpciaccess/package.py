from spack import *
from spack.pkg.builtin.libpciaccess import Libpciaccess as BuiltinLibpciaccess


class Libpciaccess(BuiltinLibpciaccess):
    __doc__ = BuiltinLibpciaccess.__doc__

    depends_on("zlib")

    def configure_args(self):
        args = super().configure_args()
        args.extend(
            (
                "--disable-dependency-tracking",
                "--enable-shared",
                "--disable-static",
                "--with-pic",
                "--with-gnu-ld",
                "--with-zlib",
            )
        )
        return args
