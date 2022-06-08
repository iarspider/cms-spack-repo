# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataSimtransportHectorproducer(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-SimTransport-HectorProducer'
    url = 'https://github.com/cms-data/SimTransport-HectorProducer/archive/V01-00-01.tar.gz'
    version('V01-00-01', sha256='d8fde77891f66a03904f255e630f8b361fd2407502d016d1b82255b5f02b6964')
    
    def url_for_version(self, version):
        url = self.url.rsplit('/', 1)[0]
        return url + '/' + str(version) + '.tar.gz'
