# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from string import Template

from spack import *


class RPMTemplate(Template):
    delimiter = "%"


xmldata = RPMTemplate(
    """<tool name="intel-vtune" version="%{realversion}">
  <info url="https://software.intel.com/en-us/intel-vtune-amplifier-xe"/>
  <client>
    <environment name="INTEL_VTUNE_BASE" default="/cvmfs/projects.cern.ch/intelsw/oneAPI/linux/x86_64/%{realversion}/vtune/latest/bin64"/>
    <environment name="BINDIR" default="$INTEL_VTUNE_BASE/bin64"/>
  </client>
  <runtime name="PATH" value="$INTEL_VTUNE_BASE/bin64" type="path"/>
  <runtime name="VTUNE_PROFILER_%{realversion}_DIR" value="$INTEL_VTUNE_BASE"/>
</tool>
"""
)


class IntelVtune(Package):
    """SCRAM config for intel vtune"""

    url = "file://" + os.path.dirname(__file__) + "/junk.xml"

    version(
        "2022",
        sha256="2cae8b754a9f824ddd27964d11732941fd88f52f0880d7f685017caba7fea6b7",
        expand=False,
    )

    def install(self, spec, prefix):
        mkdirp(prefix.etc.join("scram.d"))
        mkdirp(prefix.etc.join("profile.d"))

        with open(prefix.etc.join("scram.d/intel-vtune.xml"), "w") as f:
            f.write(xmldata.substitute(realversion=str(self.spec.version)))

        with open(prefix.etc.join("profile.d/init.sh"), "w") as f:
            f.write("INTEL_VTUNE_ROOT='{pkgrel}'".format(pkgrel=prefix))

        with open(prefix.etc.join("profile.d/init.csh"), "w") as f:
            f.write("set INTEL_VTUNE_ROOT '{pkgrel}'".format(pkgrel=prefix))
