from spack import *
from spack.pkg.builtin.py_numpy import PyNumpy as BuiltinPyNumpy


class PyNumpy(BuiltinPyNumpy):
    __doc__ = BuiltinPyNumpy.__doc__

    keep_archives = True

    @run_after('install')
    def symlink_c_api(self):
        prefix = self.spec.prefix
        mkdirp(prefix.join('c-api'))
        numpy_include = join_path(
            self.spec.prefix,
            self.spec['python'].package.platlib,
            'numpy', 'core')
        symlink(numpy_include, join_path(prefix, 'c-api', 'core'))
