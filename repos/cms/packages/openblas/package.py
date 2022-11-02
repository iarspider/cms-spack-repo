import copy

from spack import *
from spack.pkg.builtin.openblas import Openblas as BuiltinOpenblas


class Openblas(BuiltinOpenblas):
    __doc__ = BuiltinOpenblas.__doc__

    patch("OpenBLAS-fix-dynamic-arch.patch")
    patch("OpenBLAS-disable-tests.patch")

    def _microarch_target_args(self):
        make_defs = ["BINARY=64", "NUM_THREADS=256", "DYNAMIC_ARCH=0"]
        if self.spec.target.family == "x86_64":
            make_defs.append("TARGET=CORE2")
        elif self.spec.target.family == "aarch64":
            make_defs.append("TARGET=ARMV8")
        elif self.spec.target.family == "ppc64le":
            make_defs.append("CFLAGS=\"-mlong-double-64 "
                              "-mcpu=power8 -mtune=power8 ",
                              "--param=l1-cache-size=64 ",
                              "--param=l1-cache-line-size=128 ",
                              "--param=l2-cache-size=51\"")
        else:
            # Fallback to Spack behaviour
            make_defs += super()._microarch_target_args()
