import copy

from spack import *
from spack.pkg.builtin.geant4 import Geant4 as BuiltinGeant4


class Geant4(BuiltinGeant4):
    __doc__ = BuiltinGeant4.__doc__
    git = "https://github.com/cms-externals/geant4"

    version("11.0.1.cms", commit="271d2ffb2bd0a2aa26c4d15bc5e99e50f49cd232")

    drop_dependency("geant4-data")

    @BuiltinGeant4.datadir.getter
    def datadir(self):
        return ""

    def cmake_args(self):
        options = super().cmake_args()
        new_options = copy.copy(options)
        del_options = []
        for i, opt in enumerate(options):
            if opt.startswith("-DGEANT4_INSTALL_DATA"):
                del_options.insert(0, i)

        for i in del_options:
            new_options.pop(i)

        new_options.extend(
            (
                "-DGEANT4_INSTALL_EXAMPLES=OFF",
                "-DBUILD_SHARED_LIBS=ON",
                "-DBUILD_STATIC_LIBS=ON",
                "-DGEANT4_BUILD_BUILTIN_BACKTRACE=OFF",
                "-DGEANT4_BUILD_VERBOSE_CODE=OFF",
                "-DGEANT4_ENABLE_TESTING=OFF",
                '-DGEANT4_BUILD_TLS_MODEL:STRING="global-dynamic"',
                "-DCMAKE_AR=" + str(which("gcc-ar")),
                "-DCMAKE_RANLIB=" + str(which("gcc-ranlib")),
            )
        )

        return new_options
