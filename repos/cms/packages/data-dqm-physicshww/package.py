# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataDqmPhysicshww(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-DQM-PhysicsHWW'
    url = 'https://github.com/cms-data/DQM-PhysicsHWW/archive/V01-00-00.tar.gz'
    version('V01-00-00', sha256='33709ebf8ca11ef97d5ed711cce1cc4a75aa14006cad59273dba831fcb399cf7')
    
    def url_for_version(self, version):
        url = self.url.rsplit('/', 1)[0]
        return url + '/' + str(version) + '.tar.gz'
