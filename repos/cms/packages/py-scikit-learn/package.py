from spack import *
from spack.pkg.builtin.py_scikit_learn import PyScikitLearn as BuiltinPyScikitLearn


class PyScikitLearn(BuiltinPyScikitLearn):
    __doc__ = BuiltinPyScikitLearn.__doc__

    drop_depedency("py-setuptools")
    depends_on("py-setuptools", type="build")
    # depends_on("py-setuptools@:59", when="@1.0.2:", type="build") -- CMS: remove upper limit

