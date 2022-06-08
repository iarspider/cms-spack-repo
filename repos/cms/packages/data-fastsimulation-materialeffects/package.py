# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataFastsimulationMaterialeffects(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-FastSimulation-MaterialEffects'
    url = 'https://cmsrep.cern.ch/cmssw/download/data/data-FastSimulation-MaterialEffects-V05-00-00.tar.gz'
    version('V05-00-00', sha256='d77dddbd4309034191d7f73e0006de130af3023e4a17b56befc4825394cd5606')

    def url_for_version(self, version):
        url = self.url.rsplit('/', 1)[0]
        return url + '/data-FastSimulation-MaterialEffects-' + str(version) + '.tar.gz'

