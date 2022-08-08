from spack import *
from spack.pkg.builtin.rivet import Rivet as BuiltinRivet


class Rivet(BuiltinRivet):
    __doc__ = BuiltinRivet.__doc__

    patch('rivet-140-313.patch', level=0)

    @run_before('configure')
    def disable_openmp_arm(self):
        if not self.spec.satisfies('arch=aarch64'):
            return

        filter_file('^ax_openmp_flags=".*"', 'ax_openmp_flags="none"', 'configure')

    def flag_handler(self, name, flags):
        if self.spec.satisfies('@3.1.2:') and name == 'cxxflags':
            # flags.append('-faligned-new')
            flags.append('-std=c++17')
            flags.append('-g')
            if self.spec.satisfies('arch=amd64'):
                flags.append('-msse3')

            return (None, None, flags)

        return (flags, None, None)

    def configure_args(self):
        args = super().configure_args()
        args += ['--disable-doxygen', '--with-pic']
        return args
