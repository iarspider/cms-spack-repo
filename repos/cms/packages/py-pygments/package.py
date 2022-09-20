# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.py_pygments import PyPygments as BuiltinPyPygments


class PyPygments(BuiltinPyPygments):
    __doc__ = BuiltinPyPygments.__doc__

    patch("Pygments-cpp-extension-fix.patch")
