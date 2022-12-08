import os

from spack import *
from spack.pkg.builtin.python import Python as BuiltinPython


class Python(BuiltinPython):
    __doc__ = BuiltinPython.__doc__

    @run_after("install")
    def install_site_config(self):
        prefix = self.prefix
        py = "python" + str(self.spec.version.up_to(2))
        sitecfg = join_path(prefix, "lib", py, "sitecustomize.py")
        wd = os.path.dirname(__file__)
        install(join_path(wd, "sitecustomize.py"), sitecfg)
