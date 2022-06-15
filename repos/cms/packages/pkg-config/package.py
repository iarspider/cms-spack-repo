from spack import *
from spack.pkg.builtin.pkg_config import PkgConfig as BuiltinPkgConfig


class PkgConfig(BuiltinPkgConfig):
    __doc__ = BuiltinPkgConfig.__doc__

    # -- CMS hook
    drop_files = ['share/man', 'share/doc', 'share/info']

    def configure_args(self):
        args = ['--disable-shared']
        args.extend(super().configure_args())
        return args
