# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataRecobtagSoftlepton(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-RecoBTag-SoftLepton'
    url = 'https://github.com/cms-data/RecoBTag-SoftLepton/archive/V01-00-01.tar.gz'
    version('V01-00-01', sha256='c8a29ffd5ab8d923ab27413aec5163ae2417db095c6deff7a119ca595bc2c562')
    
    def url_for_version(self, version):
        url = self.url.rsplit('/', 1)[0]
        return url + '/' + str(version) + '.tar.gz'
