from spack import *
from spack.pkg.builtin.py_setuptools import PySetuptools as BuiltinPySetuptools


class PySetuptools(BuiltinPySetuptools):
    __doc__ = BuiltinPySetuptools.__doc__

    version('63.4.3', sha256='7f61f7e82647f77d4118eeaf43d64cbcd4d87e38af9611694d4866eb070cd10d', expand=False)
    version("60.9.3", sha256="2347b2b432c891a863acadca2da9ac101eae6169b1d3dfee2ec605ecd50dbfe5", expand=False)

    def install(self, spec, prefix):
        # When setuptools changes its entry point we might get weird
        # incompatibilities if building from sources in a non-isolated environment.
        #
        # https://github.com/pypa/setuptools/issues/980#issuecomment-1154471423
        #
        # We work around this issue by installing setuptools from wheels
        whl = self.stage.archive_file
        args = ["-m", "pip"] + std_pip_args + ["--prefix=" + prefix, whl]
        # CMS: inheritance is broken, we need to explicitly define python here
        # Ref: https://github.com/spack/spack/issues/31648
        # Ref: https://github.com/spack/spack/issues/32922
        python = which("python")
        python(*args)
