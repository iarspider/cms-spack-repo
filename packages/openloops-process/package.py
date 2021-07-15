# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OpenloopsProcess(Package):
    """Download process sources for OpenLoops"""

    homepage = "https://github.com/cms-externals/openloops"
    git      = "https://github.com/cms-externals/openloops.git"

    version('2.1.2', branch='cms/v2.1.2')
    patch('openloops-urlopen2curl.patch')

    depends_on('python@2.7,3.2:', type='build')
    
    def install(self, spec, prefix):
        if self.spec.satisfies('target=aarch64:'):
            filter_file('pplljj_ew', '', 'cms.coll')

        copy(join_path(os.path.dirname(__file__), 'cms.coll'), 'cms.coll') 
        downloader = Executable('./pyol/bin/download_process.py')
        downloader('cms.coll')
        install_tree('process_src', self.prefix.process_src)
        install_tree('proclib', self.prefix.proclib)
        install('cms.coll', self.prefix)