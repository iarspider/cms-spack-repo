# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

import spack
from spack import *


class CmsCommon(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    git      = "https://github.com/cms-sw/cms-common.git"

    version('1.0', commit='27f29b30619af13a2248c5c23ca6acf4fa9f5a99')

    revision = '1223'

    def patch(self):
        filter_file('SCRAMV1', 'scram', 'common/scram')
        filter_file('SCRAMV1', 'scram', 'common/scramv0')
        filter_file('SCRAMV1', 'scram', 'common/scramv1')

    def install(self, spec, prefix):
        cmsplatf = os.environ.get('SCRAM_ARCH', 'slc7_amd64_gcc900')
        if os.path.exists('.git'):
            shutil.rmtree('.git')
        for root, dirs, files in os.walk('.'):
            for fn in files:
                if os.path.isfile(join_path(root, fn)):
                    # filter_file('@CMS_PREFIX@', os.environ.get('RPM_INSTALL_PREFIX'))
                    # ^-- done in cmspost b/c RPM_INSTALL_PREFIX may be undefined at buildtime
                    filter_file('@SCRAM_ARCH@', cmsplatf, join_path(root, fn))

        install_tree('.', prefix.join(self.revision))
        install(join_path(os.path.dirname(__file__), 'cmspost.sh'), prefix)
        filter_file('cmsplatf=.*', 'cmsplatf='+cmsplatf, join_path(prefix, 'cmspost.sh'))
        filter_file('pkgrevision=.*', 'pkgrevision='+self.revision, join_path(prefix, 'cmspost.sh'))
        set_executable(join_path(prefix, 'cmspost.sh'))
