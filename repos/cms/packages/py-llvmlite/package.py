from spack import *
from spack.pkg.builtin.py_llvmlite import PyLlvmlite as BuiltinPyLlvmlite


class PyLlvmlite(BuiltinPyLlvmlite):
    __doc__ = BuiltinPyLlvmlite.__doc__

    # -- begin CMS: patches
    patch("py3-llvmlite-fpic-flag.patch", when='@0.37.0')
    patch("py3-llvmlite-removeMethod.patch", when='@0.37.0')
    patch("py3-llvmlite-version.patch", when='@0.37.0')
    # -- end CMS
