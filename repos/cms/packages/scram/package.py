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

    version('V3_00_35', commit='a5e2033a2ed7f6b84d6fd92a386a920f02bdb54b')
    version('V3_00_48', commit='e60d22b0e4e91a244ba0cf14d3a95ca48dc735c9')
    version('V3_00_36', commit='02b0bef849aa8bfc8f9c2afa5b02234221960822')
    version('V3_00_31', commit='e61917ac8b26a2fd0d9f67847aa8271ffe871671')
    version('V3_00_30', commit='16d116bf9059ce52e2deb1e58580cf55df636ca5')
    version('V3_00_29', commit='4489bd56104394c247b7cfcb64376257772e23c3')
    version('V3_00_23', commit='9794c2f7b7f2690687c41eb67778023d5c2a6e1b')

    # TODO: generate scram_arch
    scram_arch = os.environ.get('SCRAM_ARCH', 'slc7_amd64_gcc900')
    if sys.platform == 'darwin':
        scram_arch = 'osx10_amd64_clang'

    def patch(self):
        filter_file('/cms/cms-common', '/cms-common', 'SCRAM/Core/ProjectDB.py')


    def install(self, spec, prefix):
        mkdirp(join_path(prefix.etc, 'profile.d'))
        with open(join_path(prefix.etc, 'profile.d', 'init.sh'), 'w') as f:
            f.write("SCRAMV1_ROOT='{0}'\n".format(prefix))
            f.write("SCRAMV1_VERSION='{0}'\n".format(str(self.spec.version)))

        # %build
        filter_file('@CMS_PATH@', prefix,
                    join_path(self.stage.source_path, 'SCRAM', '__init__.py'))

        filter_file('@SCRAM_VERSION@', str(self.spec.version),
                    join_path(self.stage.source_path, 'SCRAM', '__init__.py'))

        filter_file('BASEPATH = .*', 'BASEPATH = "' + prefix + '"',
                    join_path(self.stage.source_path, 'SCRAM', '__init__.py'))
        # %install
        mkdirp(prefix.docs)
        install_tree(join_path('docs', 'man'), prefix.docs.man)

        mkdirp(prefix.SCRAM)
        install_tree('SCRAM', prefix.SCRAM)

        mkdirp(prefix.bin)
        install(join_path('cli', 'scram'), prefix.bin)
        install(join_path('cli', 'scram.py'), prefix.bin)

        mkdirp(join_path(prefix.etc, 'default-scram'))
        install(join_path(os.path.dirname(__file__), 'cmspost.sh'), prefix)
        cmspost = join_path(prefix, 'cmspost.sh')
        filter_file('cmsplatf=.*', f'cmsplatf={self.scram_arch}', cmspost)
        filter_file('realversion=.*', 'realversion='+str(self.spec.version), cmspost)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('SCRAM_ARCH', self.scram_arch)
        spack_env.set('SCRAMV1_ROOT', self.spec.prefix)
        spack_env.set('SCRAMV1_VERSION', str(self.spec.version))
        spack_env.unset('PYTHONHOME')
