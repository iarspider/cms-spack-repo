from spack import *
from spack.pkg.builtin.fmt import Fmt as BuiltinFmt


class Fmt(BuiltinFmt):
    __doc__ = BuiltinFmt.__doc__

    def flag_handler(self, name, flags):
        if name in ['cflags', 'cxxflags', 'cppflags']:
            if self.spec.satisfies('arch=aarch64:'):
                flags.append('CXXFLAGS=-march=armv8-a -mno-outline-atomics')
            elif self.spec.satisfies('arch=ppc64le:'):
                flags.append('CXXGLAGS=-mcpu=power8 -mtune=power8 --param=l1-cache-size=64 --param=l1-cache-line-size=128 --param=l2-cache-size=512')

        return (None, None, flags)

    def cmake_args(self):
        args = super().cmake_args()
        args.append('-DCMAKE_INSTALL_LIBDIR=lib')
        return args
