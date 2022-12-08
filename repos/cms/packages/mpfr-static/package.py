# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.mpfr import Mpfr as BuiltinMpfr


class MpfrStatic(BuiltinMpfr):
    __doc__ = BuiltinMpfr.__doc__

    def configure_args(self):
        args = super().configure_args()
        args.extend(["--disable-shared", "--enable-static"])
        return args
