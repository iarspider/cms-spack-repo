from spack import *
from spack.pkg.builtin.boost import Boost as BuiltinBoost


class Boost(BuiltinBoost):
    __doc__ = BuiltinBoost.__doc__

    git = "https://github.com/cms-externals/boost.git"
    version('1.78.0.cms', commit='7f597ea02d8a714076157b4bf65fa8e5752b8468')
