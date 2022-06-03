# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil

from spack import *


platform_tag = 'f41e221f8fb95830fc001dad975b4db770f5d29d'

class Dip(CMakePackage):
    """Put a proper description of your package here."""

    homepage = "https://www.example.com"
    # FIXME: git
    # git      = "ssh://git@gitlab.cern.ch:7999/industrial-controls/services/dip-hq/dip.git"
    # manual_download = True
    keep_archives = True
    url = 'https://cmsrep.cern.ch/cmssw/download/dip/8693f00cc422b4a15858fcd84249acaeb07b6316/dip-8693f00cc422b4a15858fcd84249acaeb07b6316.tgz'

    #FIXME: git
    version('8693f00cc422b4a15858fcd84249acaeb07b6316', sha256='bac54edf593de5b4dfabd8f9f26cb67e4bf552329a258da22b08f230259a78f6')
    #, commit='8693f00cc422b4a15858fcd84249acaeb07b6316')

    resource(name='platform',
             # FIXME: git
             # git='ssh://git@gitlab.cern.ch:7999/industrial-controls/services/dip-hq/platform-dependent.git',
             # commit='f41e221f8fb95830fc001dad975b4db770f5d29d',
             url='https://cmsrep.cern.ch/cmssw/download/dip/8693f00cc422b4a15858fcd84249acaeb07b6316/platform-dependent-f41e221f8fb95830fc001dad975b4db770f5d29d.tgz'),
             dest='platform-dependent',
             sha256='2e5baaf7689b0aa0bcf5b067c6e386aeaf7fbbbb454dd0cb7e73d56bdf970611')

    keep_archives = True
    depends_on('log4cpp')
    root_cmakelists_dir = 'platform-dependent'

    def patch(self):
        sed = which('sed')
        sed('-i', '-e', '/conanbuildinfo.cmake\|conan_basic_setup/d', 'CMakeLists.txt')
        sed('-i', '-e', '/conanbuildinfo.cmake\|conan_basic_setup/d', 'platform-dependent/CMakeLists.txt')
        f = FileFilter('CMakeLists.txt')
        f.filter('CONAN_PKG::', '')
        f.filter('log4cplus', 'log4cplusS')

    @run_after('install')
    def post_install(self):
        prefix = self.spec.prefix
        shutil.rmtree(join_path(prefix, 'lib', 'cmake'))
