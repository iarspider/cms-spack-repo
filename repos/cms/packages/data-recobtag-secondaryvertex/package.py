# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataRecobtagSecondaryvertex(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-RecoBTag-SecondaryVertex'
    url = 'https://github.com/cms-data/RecoBTag-SecondaryVertex/archive/V02-00-04.tar.gz'
    version('V02-00-04', sha256='032e5f484ebf7adf42c935918dba0aa0b01f194e40fad7fb0688562ec9f36048')
