from spack import *
from spack.pkg.builtin.re2c import Re2c as BuiltinRe2c


class Re2c(BuiltinRe2c):
    __doc__ = BuiltinRe2c.__doc__

    version('0.13.5', sha256='f3a995139af475e80a30207d02728b1e0065b0caade7375e974cb1b14861668c',
            url='https://freefr.dl.sourceforge.net/project/re2c/old/re2c-0.13.5.tar.gz')

    # -- CMS hook
    drop_files = ["share"]

    def configure_args(self):
        args = ["--disable-dependency-tracking"]
        return args
