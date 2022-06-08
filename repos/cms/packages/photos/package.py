from spack import *
from spack.pkg.builtin.photos import Photos as BuiltinPhotos


class Photos(BuiltinPhotos):
    __doc__ = BuiltinPhotos.__doc__

    keep_archives = True
