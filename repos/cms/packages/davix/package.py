from spack import *
from spack.pkg.builtin.davix import Davix as BuiltinDavix


class Davix(BuiltinDavix):
    __doc__ = BuiltinDavix.__doc__

    depends_on("curl", type=("build", "run"))

    def cmake_args(self):
        args = super().cmake_args()
        args.extend(["-DEMBEDDED_LIBCURL=FALSE", "-DDAVIX_TESTS=False"])
        return args
