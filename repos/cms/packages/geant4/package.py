import copy
import os

from spack import *
from spack.pkg.builtin.geant4 import Geant4 as BuiltinGeant4


class Geant4(BuiltinGeant4):
    __doc__ = BuiltinGeant4.__doc__
    git = "https://github.com/cms-externals/geant4"

    keep_archives = True

    version("11.0.1.cms", commit="271d2ffb2bd0a2aa26c4d15bc5e99e50f49cd232")

    drop_dependency("geant4-data")
    drop_dependency("xerces-c")
    depends_on("xerces-c", type=("build", "run"))

    def flag_handler(self, name, flags):
        arch_build_flags = []
        if self.spec.satisfies('target=aarch64:'):
            arch_build_flags = 'march=armv8-a -mno-outline-atomics'.split()
        elif self.spec.satisfies('target=ppc64le:'):
            arch_build_flags = '-mcpu=power8 -mtune=power8 --param=l1-cache-size=64 --param=l1-cache-line-size=128 --param=l2-cache-size=512'.split()

        if name in ('cflags', 'cxxflags'):
            flags.append('-fPIC')
            flags.extend(arch_build_flags)

        return (None, None, flags)

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
                '-DGEANT4_BUILD_TLS_MODEL:STRING=global-dynamic',
                "-DCMAKE_AR=" + str(which("gcc-ar")),
                "-DCMAKE_RANLIB=" + str(which("gcc-ranlib")),
            )
        )

        return new_options

    @run_after('install')
    def geant4_static(self):
        prefix = self.spec.prefix
        mkdirp(prefix.lib64.archive)
        ar = which('gcc-ar', required=True)
        with working_dir(prefix.lib64.archive):
            for fn in find(prefix.lib64, '*.a'):
                ar('x', fn)
            ofiles = find(prefix.lib64.archive, '*.o')
            ar('rcs', 'libgeant4-static.a', *ofiles)
            for fn in ofiles:
                os.unlink(fn)
