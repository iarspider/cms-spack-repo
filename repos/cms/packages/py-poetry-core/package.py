from spack import *
from spack.pkg.builtin.py_poetry_core import PyPoetryCore as BuiltinPyPoetryCore


class PyPoetryCore(BuiltinPyPoetryCore):
    __doc__ = BuiltinPyPoetryCore.__doc__

    # DUMMY DEPENDENCY - https://github.com/python-poetry/poetry/issues/6242
    depends_on("git", type="run")
