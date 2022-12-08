from spack import *
from spack.pkg.builtin.opencv import Opencv as BuiltinOpencv


class Opencv(BuiltinOpencv):
    __doc__ = BuiltinOpencv.__doc__

    version("4.5.5", sha256="a1cfdcf6619387ca9e232687504da996aaa9f7b5689986b8331ec02cb61d28ad")

    drop_patch("opencv3.4.4_cvv_cmake.patch")

    def cmake_args(self):
        super_args = super().cmake_args()

        # Remove opencv-contrib
        args = [x for x in super_args if not x.startswith("-DOPENCV_EXTRA_MODULES_PATH")]

        args += [
            self.define("CMAKE_INSTALL_LIBDIR", "lib"),
            self.define("WITH_QT", False),
            self.define("WITH_GTK", False),
            self.define("BUILD_EXAMPLES", False),
        ]
        return args
