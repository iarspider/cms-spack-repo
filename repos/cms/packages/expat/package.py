from spack import *
from spack.pkg.builtin.expat import Expat as BuiltinExpat


class Expat(BuiltinExpat):
    __doc__ = BuiltinExpat.__doc__

    version('2.1.0', sha256='823705472f816df21c8f6aa026dd162b280806838bb55b3432b0fb1fcca7eb86',
            url='https://downloads.sourceforge.net/project/expat/expat/2.1.0/' +
                'expat-2.1.0-RENAMED-VULNERABLE-PLEASE-USE-2.3.0-INSTEAD.tar.gz')

    # -- CMS hook
    drop_files = ["share"]
