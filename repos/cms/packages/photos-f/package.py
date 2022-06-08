from spack import *
from spack.pkg.builtin.photos_f import PhotosF as BuiltinPhotosF


class PhotosF(BuiltinPhotosF):
    __doc__ = BuiltinPhotosF.__doc__

    keep_archives = True
