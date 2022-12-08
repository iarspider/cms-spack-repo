from spack import *
from spack.pkg.builtin.py_requests import PyRequests as BuiltinPyRequests


class PyRequests(BuiltinPyRequests):
    __doc__ = BuiltinPyRequests.__doc__

    drop_dependency("py-charset-normalizer")
    depends_on("py-charset-normalizer", type=("build", "run"))
