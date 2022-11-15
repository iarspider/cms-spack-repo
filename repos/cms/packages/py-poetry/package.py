from spack import *
from spack.pkg.builtin.py_poetry import PyPoetry as BuiltinPyPoetry


class PyPoetry(BuiltinPyPoetry):
    __doc__ = BuiltinPyPoetry.__doc__

    drop_dependency("py-cleo")
    depends_on("py-cleo@0.8.1", type=("build", "run"))
    drop_dependency("py-crashtest")
    depends_on("py-crashtest@0.3.0:", when="^python@3.6:3", type=("build", "run"))
    drop_dependency("py-jsonschema")
    depends_on("py-jsonschema", when="@1.2:", type=("build", "run"))
