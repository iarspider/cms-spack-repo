import copy

from spack import *
from spack.pkg.builtin.pcre import Pcre as BuiltinPcre


class Pcre(BuiltinPcre):
    __doc__ = BuiltinPcre.__doc__

    # -- CMS
    depends_on('zlib')
    depends_on('bzip2')

    # -- CMS hook
    strip_files = ['lib']
    drop_files = ['share', 'lib/*.a', 'lib/*.la']
