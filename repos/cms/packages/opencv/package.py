from spack import *
from spack.pkg.builtin.opencv import Opencv as BuiltinOpencv


class Opencv(BuiltinOpencv):
    __doc__ = BuiltinOpencv.__doc__

    version("4.5.5", sha256="a1cfdcf6619387ca9e232687504da996aaa9f7b5689986b8331ec02cb61d28ad")

    def cmake_args(self):
        args = super().cmake_args()
        args += [
            self.define("CMAKE_INSTALL_LIBDIR", "lib"),
            "-DWITH_QT=OFF",
            "-DWITH_GTK=OFF",
            "-DBUILD_EXAMPLES=OFF",
        ]
        return args
