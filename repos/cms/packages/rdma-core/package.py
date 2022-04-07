import shutil

from spack import *
from spack.pkg.builtin.rdma_core import RdmaCore as BuiltinRdmaCore


class RdmaCore(BuiltinRdmaCore):
    __doc__ = BuiltinRdmaCore.__doc__
    generator = 'Ninja'
    depends_on('ninja', type='build')

    def cmake_args(self):
        args = super().cmake_args()
        args.extend(['-DENABLE_RESOLVE_NEIGH=FALSE',
                     '-DENABLE_STATIC=FALSE',
                     '-DNO_MAN_PAGES=TRUE'])

    @run_after('install')
    def post_install(self):
        prefix = self.spec.prefix
        for dir in ("bin", "etc", "lib", "libexec", "sbin", "share"):
            shutil.rmtree(join_path(prefix, dir))
