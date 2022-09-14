from spack import *
from spack.pkg.builtin.mpfr import Mpfr as BuiltinMpfr


class Mpfr(BuiltinMpfr):
    __doc__ = BuiltinMpfr.__doc__

    keep_archives = True

    @run_after('configure')
    def nodoc(self):
        touch(join_path('doc', 'mpfr.info'))
