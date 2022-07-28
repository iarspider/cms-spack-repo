from spack import *
from spack.pkg.builtin.flex import Flex as BuiltinFlex


class Flex(BuiltinFlex):
    __doc__ = BuiltinFlex.__doc__

    drop_files = ['share']  # -- CMS

    patch('gcc-flex-nonfull-path-m4.patch')

    @run_after('autoreconf')
    def disable_doc(self):
        patch_x = which('patch')
        patch_x('-p1', '-i', join_path(os.path.dirname(__file__), 'gcc-flex-disable-doc.patch'))
