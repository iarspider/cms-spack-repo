# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4ensdfstate(G4DataPackage):
    """Geant4 data for nuclides properties"""
    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4ENSDFSTATE.2.1.tar.gz"

    tags = ['hep']

    maintainers = ['drbenmorgan']

    # Only versions relevant to Geant4 releases built by spack are added
    version('2.3', sha256='9444c5e0820791abd3ccaace105b0e47790fadce286e11149834e79c4a8e9203')
    version('2.2', sha256='dd7e27ef62070734a4a709601f5b3bada6641b111eb7069344e4f99a01d6e0a6')
    version('2.1', sha256='933e7f99b1c70f24694d12d517dfca36d82f4e95b084c15d86756ace2a2790d9')
    
    g4runtime = 'G4ENSDFSTATEDATA'

    def url_for_version(self, version):
        """Handle version string."""
        return "http://geant4-data.web.cern.ch/geant4-data/datasets/G4ENSDFSTATE.%s.tar.gz" % version
