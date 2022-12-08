import os
import shutil

from spack import *
from spack.pkg.builtin.gcc import Gcc as BuiltinGcc


class Gcc(BuiltinGcc):
    __doc__ = BuiltinGcc.__doc__

    git = "https://github.com/gcc-mirror/gcc.git"
    version("11.2.1", commit="a0a0499b8bb920fdd98e791804812f001f0b4fe8")

    depends_on("flex", type="build", when="@11.2.1")
    depends_on("m4@1.4.6:", when="@11.2.1", type="build")
    depends_on("automake@1.15.1:", when="@11.2.1", type="build")
    depends_on("autoconf@2.69:", when="@11.2.1", type="build")


    keep_archives = True
    drop_files = ["share/man", "share/info", "share/doc", "share/locale", "lib*/libstdc++.a", "lib*/libsupc++.a", "lib/pkg-config"]
    strip_files = ["libexec/*/*/*/cc1", "libexec/*/*/*/cc1plus", "libexec/*/*/*/f951", "libexec/*/*/*/lto1",
        "libexec/*/*/*/collect2", "bin/*c++*", "bin/*g++*", "bin/*gcc*", "bin/*gfortran*", "bin/*gcov*", "bin/*cpp*"]

    def patch(self):
        super().patch()

        thisdir = os.path.dirname(__file__)

        if self.spec.satisfies("arch=x86_64:"):
            with open("config.gcc", "a") as f:
                print("# CMS patch to include gcc/config/i386/cms.h when building gcc", file=f)
                print("tm_file=\"$tm_file i386/cms.h\"", file=f)
                print("tm_file=\"$tm_file general-cms.h\"", file=f)

            mkdirp(join_path(self.stage.source_path, "config/i386"))
            shutil.copy(join_path(thisdir, "cms.h"), join_path(self.stage.source_path, "config/i386/cms.h"))
            shutil.copy(join_path(thisdir, "general-cms.h"), join_path(self.stage.source_path, "config/general-cms.h"))

    def configure_args(self):
        args = super().configure_args()
        conf_gcc_with_lto = ["--enable-ld=default", "--enable-lto", "--enable-gold=yes"]
        conf_gcc_arch_spec = []

        if self.spec.satisfies("arch=aarch64:"):
            conf_gcc_arch_spec = ["--enable-threads=posix", "--enable-initfini-array", "--disable-libmpx"]

        if self.spec.satisfies("arch=ppc64le:"):
            conf_gcc_arch_spec = ["--enable-threads=posix", "--enable-initfini-array", "--enable-targets=powerpcle-linux",
                "--enable-secureplt", "--with-long-double-128", "--with-cpu=power8", "--with-tune=power8", "--disable-libmpx"]

        args.extend(["--disable-dssi", "--enable-gnu-indirect-function", "--enable-__cxa_atexit", "--disable-libunwind-exceptions", "--enable-gnu-unique-object",
             "--enable-plugin", "--with-linker-hash-style=gnu", "--enable-linker-build-id", *conf_gcc_with_lto, "--enable-checking=release",
             "--enable-libstdcxx-time=rt", *conf_gcc_arch_spec, "--enable-shared", "--disable-libgcj" ])
        return args

    @run_after("install")
    def remove_lib_la(self):
        for fn in find(self.spec.prefix.lib, "*.la"):
            os.unlink(fn)

        for fn in find(self.spec.prefix.lib64, "*.la"):
            os.unlink(fn)
