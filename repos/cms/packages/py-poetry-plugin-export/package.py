from spack import *
from spack.pkg.builtin.py_poetry_plugin_export import PyPoetryPluginExport as BuiltinPyPoetryPluginExport


class PyPoetryPluginExport(BuiltinPyPoetryPluginExport):
    __doc__ = BuiltinPyPoetryPluginExport.__doc__

    # Avoid circular dependency
    drop_dependency("py-poetry")
