from spack import *
from spack.pkg.builtin.py_setuptools import PySetuptools as BuiltinPySetuptools


class PySetuptools(BuiltinPySetuptools):
    __doc__ = BuiltinPySetuptools.__doc__

    version("60.9.3", sha256="2347b2b432c891a863acadca2da9ac101eae6169b1d3dfee2ec605ecd50dbfe5", expand=False)
