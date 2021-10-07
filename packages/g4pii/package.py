# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4pii(G4DataPackage):
    """Geant4 data for shell ionisation cross-sections"""
    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4PII.1.3.tar.gz"

    tags = ['hep']

    maintainers = ['drbenmorgan']

    g4dataname = 'geant4-G4PII'
    g4runtime = 'G4PIIDATA'

    # Only versions relevant to Geant4 releases built by spack are added
    version('1.3', sha256='6225ad902675f4381c98c6ba25fc5a06ce87549aa979634d3d03491d6616e926')

    def url_for_version(self, version):
        """Handle version string."""
        return ("https://geant4-data.web.cern.ch/geant4-data/datasets/G4PII.1.3.tar.gz" % version)
