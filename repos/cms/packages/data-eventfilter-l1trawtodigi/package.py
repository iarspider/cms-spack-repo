# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataEventfilterL1trawtodigi(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-EventFilter-L1TRawToDigi'
    url = 'https://github.com/cms-data/EventFilter-L1TRawToDigi/archive/V01-00-00.tar.gz'
    version('V01-00-00', sha256='8cadf961a08fe62bbf3f8bec30c507987027f46fa47120dd8c5448b279cc5128')
