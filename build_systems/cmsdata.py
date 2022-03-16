from llnl.util.filesystem import *

from spack.package import PackageBase
from spack.directives import resource, version

import glob
import os
import re

class CMSDataPackage(Package):
    build_system_class = 'CMSDataPackage'
    phases = ['install']

    def install(self, spec, prefix):
        data = getattr(self, 'data', None) or ""
        n = self.n
        data_repo = getattr(self, 'data_repo', n.replace('data-', ''))
        data_dir = getattr(self, 'data_dir', n.replace('data-', '').replace('-', '/') + '/' + data)
        base_tool = n.upper().replace('-', '_')

        mkdirp(prefix.join(data_dir))
        install_tree('.', prefix.join(data_dir))
        mkdirp(prefix.etc.join('profile.d'))

        with open(join_path(prefix.etc.join('profile.d'), 'init.sh'), 'w') as f:
            f.write('{0}_ROOT={1}'.format(base_tool, prefix))

        with open(join_path(prefix.etc.join('profile.d'), 'init.csh'), 'w') as f:
            f.write('set {0}_ROOT {1}'.format(base_tool, prefix))

