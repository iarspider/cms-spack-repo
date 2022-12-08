from spack import *
from spack.pkg.builtin.py_cmake import PyCmake as BuiltinPyCmake


class PyCmake(BuiltinPyCmake):
    __doc__ = BuiltinPyCmake.__doc__

    drop_dependency("cmake")
    depends_on("cmake", type=("build", "link", "run")) # allow any cmake
