# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform

from spack import *


_versions = {
    'v02.04.49': {
        'Linux-aarch64': ('a02c788ea3f6a24a09a2a439488d942b2437a2ba9be1f94df59fe2f7e7137367', 'https://github.com/dmwm/dasgoclient/releases/download/v02.04.49/dasgoclient_aarch64'),
        'Linux-x86_64':  ('6daebca730e2b106c55295ecd49b7337c772c8859227c5a50a8a2336292c9d00', 'https://github.com/dmwm/dasgoclient/releases/download/v02.04.49/dasgoclient_amd64'),
        'Linux-ppc64le': ('959a87f1ec28fa899e6cb2df19851f43a1087fbc67d5f4f5f8e3ad540516ef5a', 'https://github.com/dmwm/dasgoclient/releases/download/v02.04.49/dasgoclient_ppc64le')},
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
        cmsplatf = os.environ.get('SCRAM_ARCH')

        mkdirp(join_path(prefix.etc, 'profile.d'))
        mkdirp(prefix.bin)
        install('dasgoclient_*', prefix.bin)
        install(join_path(os.path.dirname(__file__), 'dasgoclient'), prefix.etc)
        filter_file('%{cmsplatf}', cmsplatf, prefix.etc.dasgoclient)
        filter_file('%{v}', str(self.spec.version), prefix.etc.dasgoclient)
        set_executable(prefix.etc.dasgoclient)
        install(join_path(os.path.dirname(__file__), 'cmspost.sh'), prefix)
        filter_file('%{PREFIX}', prefix, join_path(prefix, 'cmspost.sh'), backup=False, string=True)
        filter_file('%v', str(spec.version), join_path(prefix, 'cmspost.sh'), backup=False, string=True)
        touch(join_path(prefix.etc, 'profile.d', 'init.sh'))
