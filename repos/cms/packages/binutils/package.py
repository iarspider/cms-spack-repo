from spack import *
from spack.pkg.builtin.binutils import Binutils as BuiltinBinutils


class Binutils(BuiltinBinutils):
    __doc__ = BuiltinBinutils.__doc__

    def configure_args(self):
        args = super().configure_args()
        args.extend(["--enable-deterministic-archives", "--enable-threads"])

        if self.spec.satisfies("target=ppc64le:"):
            args.extend(["--enable-targets=spu", "--enable-targets=powerpc-linux"])

        return args

    @run_after("build")
    def ln_to_cp(self):
        for fn in find(self.stage.source_path, "Makefile"):
            filter_file("LN = ln", "LN = cp -p", fn)
            filter_file("ln ([^-])", r"cp -p \1", fn)
