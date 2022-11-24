from spack import *
from spack.pkg.builtin.py_numba import PyNumba as BuiltinPyNumba


class PyNumba(BuiltinPyNumba):
    __doc__ = BuiltinPyNumba.__doc__

    # CMS: loosen requirement
    drop_dependency("py-llvmlite")
    depends_on("py-llvmlite@0.38:", type=("build", "run"), when="@0.56")

