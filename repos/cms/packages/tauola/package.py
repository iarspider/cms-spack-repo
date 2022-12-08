from spack import *
from spack.pkg.builtin.tauola import Tauola as BuiltinTauola


class Tauola(BuiltinTauola):
    __doc__ = BuiltinTauola.__doc__

    variant("pythia8", default=False, description="Enable pythia8 support")

    keep_archives = True

    depends_on("pythia8", when="+pythia8")

    def patch(self):
        if not self.spec.satisfies("platform=darwin"):
            return
        filter_file("-shared", "-dynamiclib -undefined dynamic_lookup", "make.inc")

    def configure_args(self):
        args = super().configure_args()
        args.extend(self.with_or_without("pythia8", "prefix"))

        return args
