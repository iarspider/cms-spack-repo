from os.path import dirname, join

from spack import *
from spack.pkg.builtin.llvm import Llvm as BuiltinLlvm


class Llvm(BuiltinLlvm):
    __doc__ = BuiltinLlvm.__doc__

    def cmake_args(self):
        args = super().cmake_args()
        args.append(self.define("LLVM_LIBDIR_SUFFIX", "64"))
        args.append(self.define("LLVM_ENABLE_PIC", True))

        compiler = Executable(self.compiler.cc)
        llvm_triple = compiler("--dumpmachine", output=str, error=str)
        args.append(self.define("LLVM_HOST_TRIPLE", llvm_triple))
        args = [x for x in args if "LLVM_REQUIRES_RTTI" not in x]
        return args
