from spack import *
from spack.pkg.builtin.fftw import Fftw as BuiltinFftw


class Fftw(BuiltinFftw):
    __doc__ = BuiltinFftw.__doc__

    strip_files = ['lib']
    drop_files = ['share']
