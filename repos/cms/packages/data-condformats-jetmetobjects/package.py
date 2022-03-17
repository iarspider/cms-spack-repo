# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataCondformatsJetmetobjects(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-CondFormats-JetMETObjects'
    url = 'https://github.com/cms-data/CondFormats-JetMETObjects/archive/V01-00-03.tar.gz'
    version('V01-00-03', sha256='ca3bd4a8450b5bd851ddbf0f75f5e6f8603dd939e97e3b6940e34de8ffd1d694')
    
    def url_for_version(self, version):
        url = self.url.rsplit('/', 1)[0]
        return url + '/' + str(version) + '.tar.gz'
