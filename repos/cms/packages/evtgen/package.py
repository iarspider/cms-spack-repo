from spack import *
from spack.pkg.builtin.evtgen import Evtgen as BuiltinEvtgen


class Evtgen(BuiltinEvtgen):
    __doc__ = BuiltinEvtgen.__doc__

    def cmake_args(self):
        args = super().cmake_args()
        args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        return args
