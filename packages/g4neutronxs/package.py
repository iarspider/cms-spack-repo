# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4neutronxs(Package):
    """Geant4 data for evaluated neutron cross-sections on natural composition
       of elements"""
    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4NEUTRONXS.1.4.tar.gz"

    tags = ['hep']

    maintainers = ['drbenmorgan']
    
    g4runtime = 'G4NEUTRONXSDATA'

    # Only versions relevant to Geant4 releases built by spack are added
    # Dataset not used after Geant4 10.4.x
    version('1.4', sha256='57b38868d7eb060ddd65b26283402d4f161db76ed2169437c266105cca73a8fd')

    def url_for_version(self, version):
        """Handle version string."""
        return "http://geant4-data.web.cern.ch/geant4-data/datasets/G4NEUTRONXS.%s.tar.gz" % version
