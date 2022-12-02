from spack import *
from spack.pkg.builtin.py_scipy import PyScipy as BuiltinPyScipy


class PyScipy(BuiltinPyScipy):
    __doc__ = BuiltinPyScipy.__doc__

    drop_dependency("py-setuptools")
    depends_on("py-setuptools", type=("build", "run"))
    drop_dependency("py-pybind11")
    depends_on("py-pybind11", type=("build", "link"))
    drop_dependency("py-pythran")
    depends_on("py-pythran", type=("build", "link"))
