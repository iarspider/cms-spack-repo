# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CmsConfig(BundlePackage):
    """Bundle package for full CMS release"""

    homepage = ""

    maintainers = ['razumov']

    version('12_0_X')

    depends_on('root')
    depends_on('coral')