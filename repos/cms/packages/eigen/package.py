import copy

from spack import *
from spack.pkg.builtin.eigen import Eigen as BuiltinEigen


class Eigen(BuiltinEigen):
    __doc__ = BuiltinEigen.__doc__

    git = 'https://github.com/cms-externals/eigen-git-mirror.git'

    version('3.4.90', commit='43d8892d117e4e76b6c472b942ebefee00bfc172')
