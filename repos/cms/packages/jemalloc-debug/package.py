from spack import *
from spack.pkg.cms.jemalloc import Jemalloc as BuiltinJemalloc


class JemallocDebug(BuiltinJemalloc):
    __doc__ = BuiltinJemalloc.__doc__
