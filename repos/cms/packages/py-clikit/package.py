from spack import *
from spack.pkg.builtin.py_clikit import PyClikit as BuiltinPyClikit


class PyClikit(BuiltinPyClikit):
    __doc__ = BuiltinPyClikit.__doc__

    drop_dependency("py-crashtest")
    depends_on(
        "py-crashtest@0.3.0:", when="^python@3.6:3", type=("build", "run")
    )  # CMS: remove upper limit
