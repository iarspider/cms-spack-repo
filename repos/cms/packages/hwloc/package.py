from spack import *
from spack.pkg.builtin.hwloc import Hwloc as BuiltinHwloc


class Hwloc(BuiltinHwloc):
    __doc__ = BuiltinHwloc.__doc__

    # -- CMS hook
    drop_files = ['lib/lib*.la', 'lib/hwloc/*.la', 'sbin', 'share/doc', 'share/hwloc', 'share/man/man1/hwloc-dump-hwdata.1']

    def configure_args(self):
        args = super().configure_args()
        args.extend((
            "--disable-static",
            "--enable-plugins=cuda,nvml",
            "--with-pic",
            "--with-gnu-ld",
            "--without-x"))
         return args

