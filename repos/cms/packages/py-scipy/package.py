from spack import *
from spack.pkg.builtin.py_scipy import PyScipy as BuiltinPyScipy


class PyScipy(BuiltinPyScipy):
    __doc__ = BuiltinPyScipy.__doc__

    drop_dependency("py-setuptools")
    depends_on("py-setuptools", when="@1.8:", type=("build", "run"))
    drop_dependency("py-pybind11")
    depends_on("py-pybind11@2.4.3:", when="@1.8:", type=("build", "link"))
