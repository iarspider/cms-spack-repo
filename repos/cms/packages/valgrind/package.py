from spack import *
from spack.pkg.builtin.valgrind import Valgrind as BuiltinValgrind


class Valgrind(BuiltinValgrind):
    __doc__ = BuiltinValgrind.__doc__

    strip_files = ['libexec', 'bin/cg_merge', 'bin/no_op*', 'bin/valgrind*']
