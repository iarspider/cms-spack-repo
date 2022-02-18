# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import os
import glob

def local_file(fn):
    return join_path(os.path.dirname(__file__), fn)

def local_file_url(fn):
    return 'file://' + local_file(fn)

class Crab(Package):
    """CRAB"""

    homepage = "https://www.example.com"

    version('1.0', url=local_file_url('crab.sh.file'), sha256='fd22c084c9b9b1aa8263d87ef48dddf6c7fef5ce2a4fc088b0426fa345ce3569', expand=False)
    resource(name='crab-proxy-package', url=local_file_url('crab-proxy-package.file'), sha256='e4744cf291b0860e69c444944625e0c53906b3e279e454e5a68b84ad9f58497e', expand=False)
    resource(name='crab-setup.csh', url=local_file_url('crab-setup.csh.file'), sha256='21e25b0dfbe25b8427411d70515993c51936a6ac182470a9f87dd0f6901438ef', expand=False)
    resource(name='crab-setup.sh', url=local_file_url('crab-setup.sh.file'), sha256='53fe8b986fb08120751cb296f5ed4072b6bcf6bf597acf69c4361713c6cc3e32', expand=False)
    resource(name='crab-env.csh', url=local_file_url('crab-env.csh.file'), sha256='addb41297aae40ef430d951a2d9d2200edd90d7e1db93bc232c133f9ae9ab17b', expand=False)
    resource(name='crab-env.sh', url=local_file_url('crab-env.sh.file'), sha256='a780ec79286446e603408179457b7f485efcc137c68cd150de05a6634f778798', expand=False)

    depends_on('crab-prod')
    depends_on('crab-pre')
    depends_on('crab-dev')

    def install(self, spec, prefix):
        directpkgreqs = []
        for dep in spec.dependencies():
            directpkgreqs.append('cms/{0}/{1}'.format(spec.name, spec.version))
    
        for fn in glob.glob(join_path(os.path.dirname(__file__), 'crab*')):
            target_fn = prefix.join(os.path.basename(fn).replace('.file', ''))
            install(fn, target_fn)
            filter_file('@CMS_PATH@', prefix, target_fn, backup=False)
            filter_file('@CRAB_COMMON_VERSION@', str(spec.version), target_fn, backup=False)
        set_executable(prefix.join('crab.sh'))
        install(local_file('cmspost.sh'), prefix)
        filter_file('%{ver}', str(spec.version), prefix.join('cmspost.sh'), backup=False)
        filter_file('directpkgreqs=.*', '"' + ' '.join(directpkgreqs) + '"', prefix.join('cmspost.sh'), backup=False)
        install(local_file('common_revision_script.sh'), prefix)
        set_executable(prefix.join('common_revision_script.sh'))
