from spack import *
from spack.pkg.builtin.opencv import Opencv as BuiltinOpencv


class Opencv(BuiltinOpencv):
    __doc__ = BuiltinOpencv.__doc__

    drop_patch("opencv3.4.4_cvv_cmake.patch")

    def cmake_args(self):
        args = super().cmake_args()

        args += [
            self.define("CMAKE_INSTALL_LIBDIR", "lib"),
            self.define("WITH_QT", False),
            self.define("WITH_GTK", False),
            self.define("BUILD_EXAMPLES", False),
        ]
        return args
