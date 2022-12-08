from spack import *
from spack.pkg.builtin.py_astroid import PyAstroid as BuiltinPyAstroid


class PyAstroid(BuiltinPyAstroid):
    __doc__ = BuiltinPyAstroid.__doc__

    drop_dependency("py-wrapt")
    # -- begin CMS: remove upper limit
    depends_on("py-wrapt@1.14:", when="@2.12.7: ^python@3.11:", type=("build", "run"))
    depends_on("py-wrapt@1.11:", when="@2.12.7: ^python@:3.10", type=("build", "run"))
    # -- end CMS

    drop_dependency("py-setuptools")
    depends_on(
        "py-setuptools@62.6:", when="@2.12.7:", type=("build", "run")
    )  # CMS: remove upper limit

