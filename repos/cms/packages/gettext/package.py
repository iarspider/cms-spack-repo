from spack import *
from spack.pkg.builtin.gettext import Gettext as BuiltinGettext


class Gettext(BuiltinGettext):
    __doc__ = BuiltinGettext.__doc__

    # -- CMS hook
    drop_files = ['share/man', 'share/doc', 'share/info']

    def configure_args(self):
        args = super().configure_args()
        args.extend((
            '--enable-relocatable',
            '--disable-silent-rules',
            '--disable-openmp',
            '--disable-rpath',
            '--disable-nls',
            '--disable-native-java',
            '--disable-acl'
        ))

        return args
