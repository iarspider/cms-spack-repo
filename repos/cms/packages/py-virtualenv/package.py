from spack import *
from spack.pkg.builtin.py_virtualenv import PyVirtualenv as BuiltinPyVirtualenv


class PyVirtualenv(BuiltinPyVirtualenv):
    __doc__ = BuiltinPyVirtualenv.__doc__

    drop_dependency("py-platformdirs")
    depends_on("py-platformdirs", type=("build", "run"))
