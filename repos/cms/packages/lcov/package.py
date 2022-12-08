from spack import *
from spack.pkg.builtin.lcov import Lcov as BuiltinLcov


class Lcov(BuiltinLcov):
    __doc__ = BuiltinLcov.__doc__

    version("1.9", url="https://kumisystems.dl.sourceforge.net/project/ltp/Coverage%20Analysis/LCOV-1.9/lcov-1.9.tar.gz", sha256="c37e125d4f0773339de3600d45ad325fe710ea2f0051d7ee2b8a168f450f1aca")
    patch("lcov-merge-files-in-same-dir.patch")

    def patch(self):
        filter_file("install -p -D", "install -p", "bin/install.sh")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make("PREFIX=%s" % prefix, "BINDIR=%s" % prefix.bin, "install")

