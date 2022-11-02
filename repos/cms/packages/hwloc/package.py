from spack import *
from spack.pkg.builtin.hwloc import Hwloc as BuiltinHwloc


def drop_patch(cls, fn):
    def filter_func(p):
        if isinstance(p, FilePatch):
            return p.relative_path != fn
        elif isinstance(p, UrlPatch):
            return p.url != fn

    old_patches = copy.deepcopy(cls.patches)
    new_patches = {}
    for spec, patches in old_patches.items():
        filtered_patches = [p for p in patches if filter_func(p)]
        if filtered_patches:
            new_patches[spec] = filtered_patches

    cls.patches = new_patches
    del old_patches
    del new_patches


def drop_dependency(cls, name):
    dependencies = {}
    for k, v in cls.dependencies.items():
        if k != name:
            dependencies[k] = v

    cls.dependencies = dependencies


def drop_conflicts(cls, name):
    conflicts = {}
    for k, v in cls.conflicts.items():
        if k != name:
            conflicts[k] = v

    cls.conflicts = conflicts


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
