from spack import *
from spack.pkg.builtin.heppdt import Heppdt as BuiltinHeppdt


class Heppdt(BuiltinHeppdt):
    __doc__ = BuiltinHeppdt.__doc__

    depends_on('intel-tbb')

    # CMS: intel-tbb dependency
    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.extend(('-O2', '-std=c++17',
                          '-I' + self.spec['intel-tbb'].prefix.include,
                          '-L' + self.spec['intel-tbb'].prefix.lib,
                          '-ltbb'))

        return (None, None, flags)
