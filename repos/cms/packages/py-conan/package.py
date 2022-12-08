from spack import *
from spack.pkg.builtin.py_conan import PyConan as BuiltinPyConan


class PyConan(BuiltinPyConan):
    __doc__ = BuiltinPyConan.__doc__

    drop_dependency("py-node-semver")
    depends_on(
        "py-node-semver@0.6.1:", type=("build", "run")
    )  # CMS: remove upper limit
    drop_dependency("py-distro")
    depends_on(
        "py-distro@1.0.2:", type=("build", "run"), when="platform=linux"
    )  # CMS: remove upper limit
