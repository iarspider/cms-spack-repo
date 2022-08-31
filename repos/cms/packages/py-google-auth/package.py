from spack import *
from spack.pkg.builtin.py_google_auth import PyGoogleAuth as BuiltinPyGoogleAuth


class PyGoogleAuth(BuiltinPyGoogleAuth):
    __doc__ = BuiltinPyGoogleAuth.__doc__

    version('2.0.2', sha256='104475dc4d57bbae49017aea16fffbb763204fa2d6a70f1f3cc79962c1a383a4')
