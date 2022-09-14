from spack import *
from spack.pkg.builtin.benchmark import Benchmark as BuiltinBenchmark


class Benchmark(BuiltinBenchmark):
    __doc__ = BuiltinBenchmark.__doc__

    keep_archives = True
    patch('google-benchmark-gcc11.patch')

    version('20211215', commit='7d03f2df490c89b2a2055e9be4e2c36db5aedd80')

    def cmake_args(self):
        args = super().cmake_args()
        args.append('-DCMAKE_INSTALL_LIBDIR=lib')
        return args
