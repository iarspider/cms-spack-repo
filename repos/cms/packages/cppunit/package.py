from spack import *
from spack.pkg.builtin.cppunit import Cppunit as BuiltinCppunit


class Cppunit(BuiltinCppunit):
    __doc__ = BuiltinCppunit.__doc__

    drop_files = ['share', 'lib/*.a', 'lib/*.la']
