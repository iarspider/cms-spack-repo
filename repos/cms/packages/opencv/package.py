from spack import *
from spack.pkg.builtin.opencv import Opencv as BuiltinOpencv


class Opencv(BuiltinOpencv):
    __doc__ = BuiltinOpencv.__doc__

    def cmake_args(self):
        args = super().cmake_args()
        args += [self.define('CMAKE_INSTALL_LIBDIR', 'lib'), '-DWITH_QT=OFF', '-DWITH_GTK=OFF', '-DBUILD_EXAMPLES=OFF']
        return args
