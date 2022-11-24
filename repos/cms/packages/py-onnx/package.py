from spack import *
from spack.pkg.builtin.py_onnx import PyOnnx as BuiltinPyOnnx


class PyOnnx(BuiltinPyOnnx):
    __doc__ = BuiltinPyOnnx.__doc__

    drop_dependency("py-protobuf")
    depends_on("py-protobuf", type=("build", "run"))
