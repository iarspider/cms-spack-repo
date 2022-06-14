from spack import *
from spack.pkg.builtin.cppunit import Cppunit as BuiltinCppunit


class Cppunit(BuiltinCppunit):
    __doc__ = BuiltinCppunit.__doc__

    def configure_args(self):
        return ['--disable-static']

