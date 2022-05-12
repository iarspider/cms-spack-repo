from spack import *
from spack.pkg.builtin.py_onnx_runtime import PyOnnxRuntime as BuiltinPyOnnxRuntime


class PyOnnxRuntime(BuiltinPyOnnxRuntime):
    __doc__ = BuiltinPyOnnxRuntime.__doc__

    def cmake_args(self):
        args = super().cmake_args()
        args.append(self.define('CMAKE_INSTALL_LIBDIR', 'lib'))
        return args
