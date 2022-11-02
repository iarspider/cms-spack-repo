import copy

from spack import *
from spack.pkg.builtin.giflib import Giflib as BuiltinGiflib


class Giflib(BuiltinGiflib):
    __doc__ = BuiltinGiflib.__doc__

    @run_after('install')
    def check_libgif_so(self):
        libgif_so = join_path(self.spec.prefix.lib, 'libgif.so')
        if os.path.islink(libgif_so) and not os.path.exists(libgif_so):
            raise InstallError('libgif.so symlink is broken')
