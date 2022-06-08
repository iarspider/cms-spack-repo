# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataSimg4cmsHgcaltestbeam(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""
    n = 'data-SimG4CMS-HGCalTestBeam'
    git = "https://github.com/cms-data/{0}.git".format(n.replace('data-', ''))
    version('V01-00-00', tag='V01-00-00')
