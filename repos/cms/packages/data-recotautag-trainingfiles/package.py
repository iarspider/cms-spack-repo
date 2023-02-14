# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DataRecotautagTrainingfiles(CMSDataPackage):
    """FIXME: Put a proper description of your package here."""

    n = "data-RecoTauTag-TrainingFiles"
    git = "https://github.com/cms-data/{0}.git".format(n.replace("data-", ""))

    version("V00-07-00", tag="V00-07-00")
    version("V00-06-00", tag="V00-06-00")
    version("V00-03-00", tag="V00-03-00")
