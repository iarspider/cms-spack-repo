import llnl.util.filesystem as fs

import spack.builder
import spack.package_base
from spack.directives import build_system, conflicts

from ._checks import (
    BaseBuilder,
    apply_macos_rpath_fixups,
)


class CMSDataPackage(spack.package_base.PackageBase):
    build_system_class = "CMSDataPackage"
    build_system("cmsdata")


@spack.builder.builder("cmsdata")
class CMSDataBuilder(BaseBuilder):
    phases = ("install",)

    def install(self, pkg, spec, prefix):
        data = getattr(pkg, "data", None) or "data"
        n = pkg.n
        data_repo = getattr(pkg, "data_repo", n.replace("data-", ""))
        data_dir = getattr(pkg, "data_dir", None)
        data_dir = data_dir or fs.join_path(data_repo.replace("-", "/"), data)

        install_root = prefix

        mkdirp(fs.join_path(install_root, data_dir))
        install_tree(".", fs.join_path(install_root, data_dir), ignore=lambda x: ".git" in x)

