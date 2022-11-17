from spack import *
from spack.pkg.builtin.py_cleo import PyCleo as BuiltinPyCleo


class PyCleo(BuiltinPyCleo):
    __doc__ = BuiltinPyCleo.__doc__

    drop_package("py-crashtest")
    depends_on(
        "py-crashtest@0.3.1:", when="@1:", type=("build", "run")
    )  # CMS: remove upper limit

