# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform

from spack import *


_versions = {
    'v02.04.46': {
        'Linux-aarch64': ('3b85ee7931d9c8cb2768ef6183a22530ed217ff0c650de071acc47501058490a', 'https://github.com/dmwm/dasgoclient/releases/download/v02.04.26/dasgoclient_aarch64'),
        'Linux-x86_64':  ('6a174b43294c122faad9c223f0a4548d0c50c56ddfa4af41b57902453950b1ce', 'https://github.com/dmwm/dasgoclient/releases/download/v02.04.26/dasgoclient_amd64'),
        'Linux-ppc64le': ('621b54ad3cd0e386ad9849b06a6b9d0db76c559ba5496515235aacfa945ddda1', 'https://github.com/dmwm/dasgoclient/releases/download/v02.04.26/dasgoclient_ppc64le')},
}

class Dasgoclient(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://github.com/dmwm/dasgoclient"

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            version(ver, sha256=pkg[0], url=pkg[1], expand=False)

    def install(self, spec, prefix):
        mkdirp(prefix.etc)
        mkdirp(prefix.bin)
        install('dasgoclient_*', prefix.bin)
        install(join_path(os.path.dirname(__file__), 'dasgoclient'), prefix.etc)
        set_executable(prefix.etc.dasgoclient)
        install(join_path(os.path.dirname(__file__), 'cmspost.sh'), prefix)
        filter_file('%{PREFIX}', prefix, join_path(prefix, 'cmspost.sh'), backup=False, string=True)
