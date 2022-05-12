# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

from spack import *
from spack.pkg.builtin.cmake import Cmake as BuiltinCmake


class Cmake(BuiltinCmake):
    __doc__ = BuiltinCmake.__doc__

    # -- CMS
    def patch(self):
        if (getattr(super(), 'patch', None) is not None):
            super().patch()
        shutil.copy(join_path(os.path.dirname(__file__), 'build-flags.cmake'), 'build-flags.cmake')
