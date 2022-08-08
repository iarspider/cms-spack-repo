from spack import *
from spack.pkg.builtin.protobuf import Protobuf as BuiltinProtobuf


class Protobuf(BuiltinProtobuf):
    __doc__ = BuiltinProtobuf.__doc__
    patch('https://raw.githubusercontent.com/cms-sw/cmsdist/IB/CMSSW_12_5_X/master/protobuf-3.15-gcc10.patch',
          sha256='e51067f65766f897e03a5e4851a8e191c98daf888653274c47de761fe8abb64b')

    def cmake_args(self):
        args = super().cmake_args()
        args += [CMakePackage.define('CMAKE_INSTALL_LIBDIR', 'lib')]
        return args
