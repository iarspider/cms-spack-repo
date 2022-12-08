from spack import *
from spack.pkg.builtin.py_grpcio_tools import PyGrpcioTools as BuiltinPyGrpcioTools


class PyGrpcioTools(BuiltinPyGrpcioTools):
    __doc__ = BuiltinPyGrpcioTools.__doc__

    drop_dependency("py-protobuf")
    depends_on(
        "py-protobuf", when="@1.48.1:", type=("build", "run")
    )  # CMS: allow any version
