from spack import *
from spack.pkg.builtin.py_matplotlib import PyMatplotlib as BuiltinPyMatplotlib


class PyMatplotlib(BuiltinPyMatplotlib):
    __doc__ = BuiltinPyMatplotlib.__doc__

    # CMS: remove upper limit
    drop_dependency("py-setuptools-scm")
    depends_on("py-setuptools-scm@4:", when="@3.5:", type="build")
