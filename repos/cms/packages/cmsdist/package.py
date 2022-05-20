# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import shutil

class Cmsdist(Package):
    """Toolfile scripts from CMSDIST repo"""

    homepage = "https://www.example.com"
    git      = "https://github.com/cms-sw/cmsdist.git"

    version('12.4.devel', commit='ec8cd99')
    version('12.4.0.pre3', tag='REL/CMSSW_12_4_0_pre3/slc7_amd64_gcc10')

    def patch(self):
        if not self.spec.satisfies('@12.4.0.pre3'):
            return
        prefix = self.stage.source_path
        filter_file('</tool>', '  <use name="veccore"/>\n</tool>',
                    join_path(prefix, 'scram-tools.file', 'tools',
                              'vecgeom', 'vecgeom.xml'))

        xmldir = join_path(prefix, 'scram-tools.file', 'tools', 'veccore')
        mkdirp(xmldir)
        tpl = """<tool name="veccore" version="@TOOL_VERSION@">
  <info url="https://github.com/root-project/veccore"/>
  <client>
    <environment name="VECCORE_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"      default="$VECCORE_BASE/include"/>
  </client>
</tool>"""

        with open(join_path(xmldir, 'veccore.xml'), 'w') as f:
            f.write(tpl)

        filter_file('export GCC_ROOT=.*',
                    'export GCC_ROOT=' + os.path.dirname(os.path.dirname(self.compiler.cc)),
                    join_path(prefix, 'scram-tools.file', 'tools', 'llvm', 'env.sh'))

    def install(self, spec, prefix):
        mkdir(prefix.join('scram-tools.file'))
        install_tree('scram-tools.file', prefix.join('scram-tools.file'))
        with working_dir(join_path(prefix, 'scram-tools.file', 'tools', 'geant4')):
            oldfile = open('env.sh').readlines()
            oldfile[1] = 'if [ "x$GEANT4_HAS_VECGEOM" != "x" ]; then'
            open('env.sh', 'w').write('\n'.join(oldfile))
