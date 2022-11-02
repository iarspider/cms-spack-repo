import copy

from spack import *
from spack.pkg.builtin.automake import Automake as BuiltinAutomake


class Automake(BuiltinAutomake):
    __doc__ = BuiltinAutomake.__doc__

    # -- CMS hook
    drop_files = ['share/man', 'share/doc', 'share/info']
