# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4incl(G4DataPackage):
    """Geant4 data for evaluated particle cross-sections on natural
    composition of elements"""
    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4INCL.1.0.tar.gz"

    tags = ['hep']

    maintainers = ['drbenmorgan']

    g4rundata = 'G4INCLDATA'

    # Only versions relevant to Geant4 releases built by spack are added
    version('1.0', sha256='716161821ae9f3d0565fbf3c2cf34f4e02e3e519eb419a82236eef22c2c4367d')

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://geant4-data.web.cern.ch/geant4-data/datasets/G4INCL.%s.tar.gz" % version)
