# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
from urllib.request import urlopen
from json import loads

from spack import *


class Cmslhetoeosmanager(Package):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    url      = "https://raw.githubusercontent.com/cms-sw/cmssw/${commit}/GeneratorInterface/LHEInterface/scripts/cmsLHEtoEOSManager.py"
    api_url  = "https://api.github.com/repos/cms-sw/cmssw/commits?path=GeneratorInterface/LHEInterface/scripts/cmsLHEtoEOSManager.py&page=0&per_page=1"

    data = loads(urlopen(api_url).read())
    commit = data[0]["sha"]
    ver = data[0]["commit"]["author"]["date"][0:10].replace("-","") + '02'

    version(ver, expand=False, sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

    def url_for_version(self, version):
        return self.url.replace('${commit}', self.commit)

    def do_fetch(self, mirror_only=False):
        config_checksum = spack.config.get('config:checksum')
        spack.config.set('config:checksum', False)
        super().do_fetch(mirror_only=mirror_only)
        spack.config.set('config:checksum', config_checksum)

    def install(self, spec, prefix):
        install_tree('.', prefix)
        install(join_path(os.path.dirname(__file__), 'cmspost.sh'), prefix)
        set_executable(join_path(prefix, 'cmspost.sh'))
        cmspost = FileFilter(join_path(prefix, 'cmspost.sh'))
        cmspost.filter('%{pkgname}', 'cmsLHEtoEOSManager', backup=False, string=True)
        cmspost.filter('%{realversion}', self.ver, backup=False, string=True)
        cmspost.filter('%{prefix}', prefix, backup=False, string=True)
