import os
import shutil

from spack import *
from spack.pkg.builtin.flex import Flex as BuiltinFlex


class Flex(BuiltinFlex):
    __doc__ = BuiltinFlex.__doc__

    drop_files = ["share"]  # -- CMS

    patch("gcc-flex-disable-doc.patch")
    patch("gcc-flex-nonfull-path-m4.patch")

    drop_dependency("help2man")

    drop_patch("https://github.com/westes/flex/commit/24fd0551333e7eded87b64dd36062da3df2f6380.patch?full_index=1")
    drop_dependency("gettext")

    def autoreconf(self,spec,version):
        # TODO: why is configure renamed?

        shutil.move(join_path(self.stage.source_path, "configure.orig"), join_path(self.stage.source_path, "configure"))
        return
