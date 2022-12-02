from spack import *
from spack.pkg.builtin.openldap import Openldap as BuiltinOpenldap


class Openldap(BuiltinOpenldap):
    __doc__ = BuiltinOpenldap.__doc__

    version("2.4.45", sha256="cdd6cffdebcd95161a73305ec13fc7a78e9707b46ca9f84fb897cd5626df3824")
