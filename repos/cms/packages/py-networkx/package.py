from spack import *
from spack.pkg.builtin.py_networkx import PyNetworkx as BuiltinPyNetworkx


class PyNetworkx(BuiltinPyNetworkx):
    __doc__ = BuiltinPyNetworkx.__doc__

    drop_dependency("py-scipy")
    depends_on("py-scipy", type=("build", "run"))
