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
    # 
    depends_on('oracle-instant-client@19.11.0.0.0', when='target=x86_64:')
    depends_on('oracle-instant-client@19.10.0.0.0', when='target=arm64')
    depends_on('oracle-instant-client@19.3.0.0.0', when='target=ppc64le')
