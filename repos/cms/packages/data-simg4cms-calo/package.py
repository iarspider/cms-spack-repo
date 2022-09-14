# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataSimg4cmsCalo(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-SimG4CMS-Calo'
    url = "http://cmsrep.cern.ch/cmssw/download/data/data-SimG4CMS-Calo-V03-04-00.tar.gz"
    version('V03-04-00', sha256='1adbf43365baa1c28582243ba59569a7f1006cb967698dedf4841325e21ba16b')

    def url_for_version(self, version):
        url = self.url.rsplit('/', 1)[0]
        return url + '/data-SimG4CMS-Calo-' + str(version) + '.tar.gz'
