from spack import *
from spack.pkg.builtin.xgboost import Xgboost as BuiltinXgboost


class Xgboost(BuiltinXgboost):
    __doc__ = BuiltinXgboost.__doc__

    patch('xgboost-arm-and-ppc.patch', when='target=aarch64:')
    patch('xgboost-arm-and-ppc.patch', when='target=ppc64le:')