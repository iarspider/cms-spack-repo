from spack import *
from spack.pkg.builtin.py_jupyter_packaging11 import PyJupyterPackaging11 as BuiltinPyJupyterPackaging11


class PyJupyterPackaging11(BuiltinPyJupyterPackaging11):
    __doc__ = BuiltinPyJupyterPackaging11.__doc__

    version("0.12.3", sha256="9d9b2b63b97ffd67a8bc5391c32a421bc415b264a32c99e4d8d8dd31daae9cf4")
    depends_on("py-hatchling@0.25:", when="@0.12.3:", type="build")

