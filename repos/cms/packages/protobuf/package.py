from spack import *
from spack.pkg.builtin.protobuf import Protobuf as BuiltinProtobuf


class Protobuf(BuiltinProtobuf):
    __doc__ = BuiltinProtobuf.__doc__

    def cmake_args(self):
        args = super().cmake_args()
        args += [CMakePackage.define('CMAKE_INSTALL_LIBDIR', 'lib')]
        return args
