from spack import *
from spack.pkg.builtin.py_tensorboard import PyTensorboard as BuiltinPyTensorboard


class PyTensorboard(BuiltinPyTensorboard):
    __doc__ = BuiltinPyTensorboard.__doc__

    drop_dependency("py-google-auth-oauthlib")
    depends_on(
        "py-google-auth-oauthlib@0.4.1:", type=("build", "run")
    )  #  CMS: remove upper limit

    drop_dependency("py-google-auth")
    depends_on(
        "py-google-auth", type=("build", "run")
    )  #  CMS: remove limit

    drop_dependency("py-protobuf")
    depends_on(
        "py-protobuf", type=("build", "run"), when="@2.9:"
    )  # CMS: any version will do
