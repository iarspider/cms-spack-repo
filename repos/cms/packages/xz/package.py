from spack import *
from spack.pkg.builtin.xz import Xz as BuiltinXz


class Xz(BuiltinXz):
    __doc__ = BuiltinXz.__doc__

    # -- CMS hooks
    strip_files = ['lib']
    drop_files = ['share']

    def configure_args(self):
        args = ['--disable-nls', '--disable-doc']  # -- CMS
        args.extend(super().configure_args())

        return args

    def flag_handler(self, name, flags):
        if name == 'cflags' and '+pic' in self.spec:
            flags = super().flag_handler(name, flags)[0]
            flags.append('-Ofast')  # -- CMS
        return (flags, None, None)
