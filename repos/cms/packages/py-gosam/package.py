from spack import *
from spack.pkg.builtin.py_gosam import PyGosam as BuiltinPyGosam


class PyGosam(BuiltinPyGosam):
    __doc__ = BuiltinPyGosam.__doc__

    version(
        "2.1.0",
        url="https://github.com/gudrunhe/gosam/releases/download/2.1.0/gosam-2.1.0-93fd8c5.tar.gz",
        sha256="1b42d4502a1fed1244d5149305af1e7d4bf7089344046f23a6b3285d23172576",
    )

    def flag_handler(self, name, flags):
        if name in ["cflags", "cxxflags", "cppflags"]:
            flags.append(self.compiler.cxx_pic_flag)
            return (flags, None, None)
        elif name == "cflags":
            flags.append(self.compiler.cc_pic_flag)
            return (flags, None, None)

        return (None, flags, None)
