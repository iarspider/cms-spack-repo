from spack import *
from spack.pkg.builtin.freetype import Freetype as BuiltinFreetype


class Freetype(BuiltinFreetype):
    __doc__ = BuiltinFreetype.__doc__

   strip_files = ['lib']

    # -- CMS
    @run_after('install')
    def darwin_post(self):
        spec = self.spec
        prefix = self.prefix

        if spec.platform == 'darwin':
            install_name_tool = Executable('install_name_tool')
            install_name_tool('-id', join_path(prefix, 'lib', 'libfreetype-cms.dylib'), '-change', join_path(prefix, 'lib', 'libfreetype.6.dylib'),
                              join_path(prefix, 'lib', 'libfreetype-cms.dylib'), join_path(prefix, 'lib', 'libfreetype.6.dylib'))
            with working_dir(prefix):
                os.symlink('libfreetype.6.dylib', join_path('lib', libfreetype-cms.dylib))

            filter_file('-lfreetype', '-lfreetype-cms', join_path(prefix, 'bin', freetype-config))

