# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Utm(AutotoolsPackage):
    """UTM is a C++ library for reading Level-1 XML trigger menus
       and translating them into an event setup used for emulation
       and Level-1 trigger firmware creation."""

    homepage = "https://globaltrigger.web.cern.ch/globaltrigger/release/utm/latest_doc/html/userGuide/intro.html"
    git      = "https://gitlab.cern.ch/cms-l1t-utm/utm.git"

    version('utm_0.10.0', tag='utm_0.10.0')

    depends_on('xerces-c')
    depends_on('boost')
    depends_on('gmake', type='build')

    def setup_build_environment(self, env):
        env.set('XERCES_C_BASE', self.spec['xerces-c'].prefix)
        env.set('BOOST_BASE', self.spec['boost'].prefix)

    def install(self, spec, prefix):
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        install_tree('xsd-type', prefix.join('xsd-type'))
        install_tree('menu.xsd', prefix.join('menu.xsd'))
