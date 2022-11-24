from spack import *
from spack.pkg.builtin.py_protobuf import PyProtobuf as BuiltinPyProtobuf


class PyProtobuf(BuiltinPyProtobuf):
    __doc__ = BuiltinPyProtobuf.__doc__

    # CMS: allow any version
    drop_dependency("protobuf")
    depends_on("protobuf")

