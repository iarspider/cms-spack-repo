from spack import *
from spack.pkg.builtin.py_sqlalchemy import PySqlalchemy as BuiltinPySqlalchemy


class PySqlalchemy(BuiltinPySqlalchemy):
    __doc__ = BuiltinPySqlalchemy.__doc__

    patch('py3-sqlalchemy-1.3.24-add-frontier-dialect.patch')
    patch('py3-sqlalchemy-1.3.24-fix-sqlite-dialect-timestamp.patch')
    patch('py3-sqlalchemy-1.3.24-server_version_info.patch')
