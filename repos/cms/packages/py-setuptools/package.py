from spack import *
from spack.pkg.builtin.py_setuptools import PySetuptools as BuiltinPySetuptools


class PySetuptools(BuiltinPySetuptools):
    __doc__ = BuiltinPySetuptools.__doc__

    version('63.4.3', sha256='7f61f7e82647f77d4118eeaf43d64cbcd4d87e38af9611694d4866eb070cd10d', expand=False)
    version("60.9.3", sha256="2347b2b432c891a863acadca2da9ac101eae6169b1d3dfee2ec605ecd50dbfe5", expand=False)
