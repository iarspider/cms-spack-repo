from spack import *
from spack.pkg.builtin.hepmc import Hepmc as BuiltinHepmc


class Hepmc(BuiltinHepmc):
    __doc__ = BuiltinHepmc.__doc__

    def cmake_args(self):
        args = super().cmake_args()
        args.append('-fPIC')
        return args

    @run_after('install')
    def post_install(self):
        prefix = self.prefix
        for fn in glob.glob(join_path(prefix.lib, '*.so')):
            os.remove(fn)
