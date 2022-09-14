from spack import *
from spack.pkg.cms.jemalloc import Jemalloc as CMSJemalloc


class JemallocDebug(CMSJemalloc):
    __doc__ = CMSJemalloc.__doc__

    def configure_args(self):
        args = super().configure_args()
        args.extend(('--enable-debug', '--enable-fill'))
        return args
