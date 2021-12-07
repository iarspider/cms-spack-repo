# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class Cms(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "foobar"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    # FIXME: Add proper versions and checksums here.
    # version('1.2.3', '0123456789abcdef0123456789abcdef')

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    url = 'file://' + os.path.dirname(__file__) + '/../ToolfilePackage/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False) 

    stages = ['install']

    def install(self, spec, prefix): 
       mkdirp(prefix.include.foo)
       mkdirp(join_path(self.stage.source_path, 'include/foo'))
       f = open(join_path(self.stage.source_path, 'include', 'a.h'), 'w')
       f.close()
       f = open(join_path(self.stage.source_path, 'include/foo', 'b.h'), 'w')
       f.close()

       install_tree(join_path(self.stage.source_path, 'include'), prefix.include)
