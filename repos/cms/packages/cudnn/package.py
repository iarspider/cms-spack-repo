import shutil

from spack import *
from spack.pkg.builtin.cudnn import Cudnn as BuiltinCudnn


class Cudnn(BuiltinCudnn):
    __doc__ = BuiltinCudnn.__doc__

    @run_after('install')
    def post_install(self):
        # -- CMS: remove static libraries
        for fn in glob.glob(prefix.lib.join('*.a')):
            os.unlink(fn)

        # -- CMS: remove static libraries
        for fn in glob.glob(prefix.lib.join('*.a')):
            os.unlink(fn)

        # -- CMS: onnxruntime is hardcoded to look for the cudnn libraries under .../lib64
        shutil.move(prefix.lib, prefix.lib64)
