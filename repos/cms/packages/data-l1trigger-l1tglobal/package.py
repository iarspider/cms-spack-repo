# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataL1triggerL1tglobal(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-L1Trigger-L1TGlobal'
    url = 'https://github.com/cms-data/L1Trigger-L1TGlobal/archive/V00-00-07.tar.gz'

    version('V00-02-00', sha256='3dc816a13f22ba592309ebb8a55796c28d0dae487fba998208372310ddf1ab9c')
    version('V00-00-07', sha256='9b3732a938d6032b80419c8e573eee77d0918390c0904ccfdea7cbc5de82962e')

    def url_for_version(self, version):
        url = self.url.rsplit('/', 1)[0]
        return url + '/' + str(version) + '.tar.gz'
