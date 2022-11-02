import copy

from spack import *
from spack.pkg.builtin.gsl import Gsl as BuiltinGsl


class Gsl(BuiltinGsl):
    __doc__ = BuiltinGsl.__doc__

    # CMS
    @run_after('install')
    def move_cblas(self):
        mkdirp(join_path(self.spec.prefix, 'cblas'))
        for fn in glob.glob(join_path(self.spec.prefix.lib, 'libgslcblas*')):
            shutil.move(fn, join_path(self.spec.prefix, 'cblas'))

    # CMS
    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('GSL_CBLAS_LIB', '-L{0} -lopenblas'.format(self.spec['openblas'].prefix.lib))
