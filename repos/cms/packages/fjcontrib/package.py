from spack import *
from spack.pkg.builtin.fjcontrib import Fjcontrib as BuiltinFjcontrib


class Fjcontrib(BuiltinFjcontrib):
    __doc__ = BuiltinFjcontrib.__doc__

    variant("cms", default=False, description="Apply CMS patch")
    patch("cms.patch", when="+cms")
