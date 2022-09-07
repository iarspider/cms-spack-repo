from spack import *
from spack.pkg.builtin.py_sqlalchemy import PySqlalchemy as BuiltinPySqlalchemy


class PySqlalchemy(BuiltinPySqlalchemy):
    __doc__ = BuiltinPySqlalchemy.__doc__

    version('1.3.24', sha256='ebbb777cbf9312359b897bf81ba00dae0f5cb69fba2a18265dcc18a6f5ef7519')

    patch('py3-sqlalchemy-1.3.24-add-frontier-dialect.patch')
    patch('py3-sqlalchemy-1.3.24-fix-sqlite-dialect-timestamp.patch')
    patch('py3-sqlalchemy-1.3.24-server_version_info.patch')
