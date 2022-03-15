# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataL1triggerL1tglobal(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-L1Trigger-L1TGlobal'
    url = 'https://github.com/cms-data/L1Trigger-L1TGlobal/archive/V00-00-07.tar.gz'
    version('V00-00-07', sha256='9b3732a938d6032b80419c8e573eee77d0918390c0904ccfdea7cbc5de82962e')
