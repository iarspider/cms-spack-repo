from spack import *
from spack.pkg.builtin.oracle_instant_client import OracleInstantClient as BuiltinOracleInstantClient
from spack.pkg.builtin.oracle_instant_client import oracleclient_releases

import os
import platform
import shutil


class OracleInstantClient(BuiltinOracleInstantClient):
    __doc__ = BuiltinOracleInstantClient.__doc__

    releases = oracleclient_releases()
    key = "{0}-{1}".format(platform.system(), platform.machine())
    for release in releases:
        if platform.machine() == 'x86_64':
            # -- CMS: OCCI lib with new C++ ABI (GCC 5 and above)
            resource(name='occi_lib', url='http://cmsrep.cern.ch/cmssw/download/oracle-mirror/x64/libocci.so.19.1.zip',
                     sha256='f5c9031944a12543f2c61e0f65b00a4cb2b62cd152579679d37c780b93653718',
                     when='@19.3.0.0:19.11.9.9 ', placement='occi_lib')

    @run_after('install')
    def move_occi_lib(self):
        prefix = self.spec.prefix
        if os.path.exists(join_path(prefix.lib, 'libocci_gcc53.so.19.1')):
            shutil.move(join_path(prefix.lib, 'libocci_gcc53.so.19.1'), join_path(prefix.lib, 'libocci.so.19.1'))

