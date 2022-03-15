# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataRecobtagCtagging(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-RecoBTag-CTagging'
    url = 'https://github.com/cms-data/RecoBTag-CTagging/archive/V01-00-03.tar.gz'
    version('V01-00-03', sha256='58f7464d1c17c8688f4f8060d9c5f53c3665a41d63109a7a772f45ddc261b1d7')
