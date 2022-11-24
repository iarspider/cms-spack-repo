from spack import *
from spack.pkg.builtin.py_pylint import PyPylint as BuiltinPyPylint


class PyPylint(BuiltinPyPylint):
    __doc__ = BuiltinPyPylint.__doc__

    drop_dependency("py-setuptools")
    depends_on(
        "py-setuptools@62.6:", when="@2.15.0:", type="build"
    )  # CMS: remove upper limit

