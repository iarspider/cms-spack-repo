# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import shutil
import os
import glob


class Mcfm(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    git      = "https://github.com/cms-externals/MCFM.git"

    version('6.3', branch='cms/6.3', commit='d2e025c')
    keep_archives = True # -- CMS

    depends_on('root')
    patch('mcfm-6.3-opt-for-size.patch', when='target=aarch64:')
    patch('mcfm.patch')

    def edit(self, spec, prefix):
#        filter_file('FFLAGS 	=', 'FFLAGS 	= -std=legacy ', 'makefile')
#        filter_file('F90FLAGS 	=', 'F90FLAGS 	= -std=legacy ', 'makefile')

#        filter_file('FFLAGS =', 'FFLAGS  = -std=legacy ', 'QCDLoop/makefile')
#        filter_file('F77FLAGS', 'FFLAGS', 'QCDLoop/makefile')
        filter_file('$(PWD)', '$(CURDIR)', 'QCDLoop/makefile', string=True)
        return

    def build(self, spec, prefix):
        mkdirp('obj')
        make('-C', 'QCDLoop')

        make()
        shutil.move('Bin', 'bin')

        mkdirp('lib')
        ar = which('ar')
        with open('libMCFM.txt', 'w') as f:
            for fn in glob.glob(join_path('obj', '*.o')):
                f.write(fn + '\n')
        ar('cr', join_path('lib', 'libMCFM.a'), '@libMCFM.txt')

    def install(self, spec, prefix):
        os.remove(join_path('bin', 'mcfm'))
        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
