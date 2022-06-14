from spack import *
from spack.pkg.builtin.gdb import Gdb as BuiltinGdb


class Gdb(BuiltinGdb):
    __doc__ = BuiltinGdb.__doc__

    depends_on('expat')  # -- CMS
    depends_on('zlib')  # -- CMS

    drop_files = ['lib', 'bin/gdbserver', 'bin/gdbtui', 'share/man', 'share/info', 'share/locale']  # -- CMS

    def configure_args(self):
        args = super().configure_args()
        args.extend(('--with-expat', '--with-zlib'))

        args.append('CFLAGS=-Wno-error=strict-aliasing')
        if '~doc' in self.spec:
            args.append('MAKEINFO=true')

        return args
