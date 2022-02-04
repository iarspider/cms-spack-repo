# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class OpenloopsProcess(Package):
    """Download process sources for OpenLoops"""

    homepage = "https://github.com/cms-externals/openloops"
    git      = "https://github.com/cms-externals/openloops.git"

    version('2.1.2', branch='cms/v2.1.2')
    patch('openloops-urlopen2curl.patch')

    variant('tiny', default=False, description='Only download one process to speed things up')

    depends_on('python@2.7,3.2:', type='build')
    
    def install(self, spec, prefix):
        coll_file = 'cms.coll' if not self.spec.variants['tiny'].value else 'tiny.coll'
        if self.spec.satisfies('target=aarch64:'):
            filter_file('pplljj_ew', '', coll_file)

        copy(join_path(os.path.dirname(__file__), coll_file), coll_file) 
        downloader = Executable('./pyol/bin/download_process.py')
        downloader(coll_file)
        install_tree('process_src', self.prefix.process_src)
        install_tree('proclib', self.prefix.proclib)
        install(coll_file, self.prefix)
