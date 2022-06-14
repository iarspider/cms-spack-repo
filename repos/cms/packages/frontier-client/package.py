from spack import *
from spack.pkg.builtin.frontier_client import FrontierClient as BuiltinFrontierClient


class FrontierClient(BuiltinFrontierClient):
    __doc__ = BuiltinFrontierClient.__doc__

    git = "https://github.com/cms-externals/frontier_client.git"
    version('2.9.1.cms', commit='7259a2c8efaf79b5d2ca78cb7f3bb39318ff4400')
