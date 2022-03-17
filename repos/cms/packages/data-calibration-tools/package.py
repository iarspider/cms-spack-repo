# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataCalibrationTools(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-Calibration-Tools'
    homepage = 'https://example.com'
    url = 'https://github.com/cms-data/Calibration-Tools/archive/V01-00-00.tar.gz'
    version('V01-00-00', sha256='3bbe64ce8f2a31ce8ec23028a49c5090028a33678fb84b61b19a823d31a3664e')

    def url_for_version(self, version):
        url = self.url.rsplit('/', 1)[0]
        fname = str(version) + '.tar.gz'

        return url  + '/' + fname

