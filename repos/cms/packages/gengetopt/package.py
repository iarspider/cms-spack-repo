from spack import *
from spack.pkg.builtin.gengetopt import Gengetopt as BuiltinGengetopt


class Gengetopt(BuiltinGengetopt):
    __doc__ = BuiltinGengetopt.__doc__

    patch('gengetopt-parallelbuild.patch')

    drop_files = ['share']
    force_autoreconf = True

    parallel = True
