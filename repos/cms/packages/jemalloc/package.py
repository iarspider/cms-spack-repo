from spack import *
from spack.pkg.builtin.jemalloc import Jemalloc as BuiltinJemalloc


class Jemalloc(BuiltinJemalloc):
    __doc__ = BuiltinJemalloc.__doc__
    git = "https://github.com/cms-externals/jemalloc.git"
    version('5.2.1.cms', commit="de1caefb587217f0b519eb425d7a9b3570e5ba28")
