from spack import *
from spack.pkg.builtin.bison import Bison as BuiltinBison


class Bison(BuiltinBison):
    __doc__ = BuiltinBison.__doc__

    # -- CMS
    drop_files = ["share/man", "share/locale", "share/info"]

    def configure_args(self):
        return ['--disable-nls', '--enable-dependency-tracking']
