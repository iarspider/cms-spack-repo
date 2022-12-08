from spack import *
from spack.pkg.builtin.py_keras import PyKeras as BuiltinPyKeras


class PyKeras(BuiltinPyKeras):
    __doc__ = BuiltinPyKeras.__doc__

    drop_dependency("py-scipy")
    depends_on("py-scipy", type=("build", "run"))

    drop_dependency("protobuf")
    depends_on("protobuf", type=("build", "link", "run"))

    drop_dependency("py-tensorboard")
    depends_on("py-tensorboard", type=("build", "run"))
