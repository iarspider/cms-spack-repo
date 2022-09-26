from spack import *
from spack.pkg.builtin.py_numba import PyNumba as BuiltinPyNumba


class PyNumba(BuiltinPyNumba):
    __doc__ = BuiltinPyNumba.__doc__

    version("0.56.2", sha256="3492f0a5d09e257fc521f5377a6c6b907eec1920d14739f0b2458b9d29946a5a")
    depends_on("py-llvmlite@0.38.1", type=("build", "run"))
