from spack import *
from spack.pkg.builtin.benchmark import Benchmark as BuiltinBenchmark


class Benchmark(BuiltinBenchmark):
    __doc__ = BuiltinBenchmark.__doc__

    keep_archives = True
    patch('google-benchmark-gcc11.patch')

    def cmake_args(self):
        args = super().cmake_args()
        args.append('-DCMAKE_INSTALL_LIBDIR=lib')
        return args
