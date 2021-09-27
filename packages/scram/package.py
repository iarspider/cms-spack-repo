from spack import *
from glob import glob
from string import Template
import re
import fnmatch
import shutil
import sys,os


class Scram(Package):
    """SCRAM as used by CMS"""

    homepage = "https://github.com/cms-sw/SCRAM"
    url = "https://github.com/cms-sw/SCRAM/archive/V2_2_6.tar.gz"
    git = "https://github.com/cms-sw/SCRAM.git"

    version('3.0.31', commit='e61917ac8b26a2fd0d9f67847aa8271ffe871671')
    version('3.0.30', commit='16d116bf9059ce52e2deb1e58580cf55df636ca5')
    version('3.0.29', commit='4489bd56104394c247b7cfcb64376257772e23c3')
    version('3.0.23', commit='9794c2f7b7f2690687c41eb67778023d5c2a6e1b')

    # TODO: generate scram_arch
    scram_arch = 'slc7_amd64_gcc930'
    if sys.platform == 'darwin':
        scram_arch = 'osx10_amd64_clang'

    def install(self, spec, prefix):
        # %build
        filter_file('@CMS_PATH@', prefix,
                    join_path(self.stage.source_path, 'SCRAM', '__init__.py'))

        filter_file('@SCRAM_VERSION@', str(self.spec.version),
                    join_path(self.stage.source_path, 'SCRAM', '__init__.py'))

        filter_file('BASEPATH = .*', 'BASEPATH = "' + prefix + '"',
                    join_path(self.stage.source_path, 'SCRAM', '__init__.py'))
        # %install
        mkdirp(prefix.bin)
        mkdirp(prefix.SCRAM)
        install_tree('SCRAM', prefix.SCRAM)
        install(join_path('cli', 'scram'), prefix.bin)
        install(join_path('cli', 'scram.py'), prefix.bin)

        # %post
        mkdirp(join_path(prefix, 'etc', 'profile.d'))
        with open(join_path(prefix, 'etc', 'profile.d', 'init.sh'), 'w') as f:
            f.write("SCRAMV1_ROOT='"+prefix+"'\n")
            f.write("SCRAMV1_VERSION='"+str(self.spec.version)+"'\n")

        with open(join_path(prefix, 'etc', 'profile.d', 'init.csh'), 'w') as f:
            f.write("set SCRAMV1_ROOT='"+prefix+"'\n")
            f.write("set SCRAMV1_VERSION='"+str(self.spec.version)+"'\n")

        with working_dir(prefix.etc.scramrc, create=True):
            touch('links.db')
            with open('cmssw.map', 'w') as f:
                f.write('CMSSW='+self.scram_arch+'/cms/cmssw/CMSSW_*\n')

            with open('cmssw-patch.map', 'w') as f:
                f.write('CMSSW='+self.scram_arch+'/cms/cmssw-patch/CMSSW_*\n')

            with open('coral.map', 'w') as f:
                f.write('CORAL='+self.scram_arch+'/cms/coral/CORAL_*\n')

            # TODO: OldDB
            touch('site.cfg')

        mkdirp(join_path(prefix.etc, 'default-scram'))

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('SCRAM_ARCH', self.scram_arch)
        spack_env.set('SCRAMV1_ROOT', self.spec.prefix)
        spack_env.set('SCRAMV1_VERSION', str(self.spec.version))
