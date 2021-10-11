# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4saiddata(G4DataPackage):
    """Geant4 data from evaluated cross-sections in SAID data-base """
    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4SAIDDATA.1.1.tar.gz"

    tags = ['hep']

    g4dataname = 'geant4-G4SAIDDATA'
    g4runtime = 'G4SAIDXSDATA'

    maintainers = ['drbenmorgan']

    # Only versions relevant to Geant4 releases built by spack are added
    version('2.0', sha256='1d26a8e79baa71e44d5759b9f55a67e8b7ede31751316a9e9037d80090c72e91')
    version('1.1', sha256='a38cd9a83db62311922850fe609ecd250d36adf264a88e88c82ba82b7da0ed7f')

    def url_for_version(self, version):
        """Handle version string."""
        return "http://geant4-data.web.cern.ch/geant4-data/datasets/G4SAIDDATA.%s.tar.gz" % version
