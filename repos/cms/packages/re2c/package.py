from spack import *
from spack.pkg.builtin.re2c import Re2c as BuiltinRe2c


class Re2c(BuiltinRe2c):
    __doc__ = BuiltinRe2c.__doc__

    # -- CMS hook
    drop_files = ["share"]

    def configure_args(self):
        args = ["--disable-dependency-tracking"]
        return args
