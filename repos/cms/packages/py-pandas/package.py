from spack import *
from spack.pkg.builtin.py_pandas import PyPandas as BuiltinPyPandas


class PyPandas(BuiltinPyPandas):
    __doc__ = BuiltinPyPandas.__doc__

    def patch(self):
        if getattr(super(), "patch", None):
            super().patch()

        if self.spec.satisfies("@1.4.4"):
            filter_file("#include <stdint.h>", "#include_next <stdint.h>", "pandas/_libs/src/headers/stdint.h", string=True)
