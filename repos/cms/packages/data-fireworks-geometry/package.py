# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataFireworksGeometry(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-Fireworks-Geometry'
    git = "https://github.com/cms-data/{0}.git".format(n.replace('data-', ''))
    version('V07-06-00', tag='V07-06-00')
    resource(url='http://cmsrep.cern.ch/cmssw/download/Fireworks-Geometry/20200401/cmsGeom2026.root',
             sha256='3077e4d9abd62c57d1d71b30fa968ba52a7c12879a7fc71d90d94c4123e426fa',
             placement={'cmsGeom2026.root': 'cmsGeom2026.root'})
