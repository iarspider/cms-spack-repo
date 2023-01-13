from spack import *
from spack.pkg.builtin.hwloc import Hwloc as BuiltinHwloc


class Hwloc(BuiltinHwloc):
    __doc__ = BuiltinHwloc.__doc__

    def configure_args(self):
        args = super().configure_args()
        plugins = []
        if "+cuda" in self.spec:
            plugins.append("cuda")
        if "+rocm" in self.spec:
            plugins.append("rsmi")
        if "+nvml" in self.spec:
            plugins.append("nvml")
        if plugins:
            args.append("--enable-plugins=" + ",".join(plugins))

        return args
