import copy

from spack import *
from spack.pkg.builtin.py_skl2onnx import PySkl2onnx as BuiltinPySkl2onnx


class PySkl2onnx(BuiltinPySkl2onnx):
    __doc__ = BuiltinPySkl2onnx.__doc__

    # CMS: remove upper bound
    drop_dependency("py-scikit-learn")
    depends_on("py-scikit-learn@0.19:")
