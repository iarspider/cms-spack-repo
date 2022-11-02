import copy

from spack import *
from spack.pkg.builtin.py_gosam import PyGosam as BuiltinPyGosam


class PyGosam(BuiltinPyGosam):
    __doc__ = BuiltinPyGosam.__doc__

    def flag_handler(self, name, flags):
        if name in ["cflags", "cxxflags", "cppflags"]:
            flags.append(self.compiler.cxx_pic_flag)
            return (flags, None, None)
        elif name == "cflags":
            flags.append(self.compiler.cc_pic_flag)
            return (flags, None, None)

        return (None, flags, None)
