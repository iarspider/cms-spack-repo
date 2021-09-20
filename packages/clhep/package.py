# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Clhep(CMakePackage):
    """CLHEP is a C++ Class Library for High Energy Physics. """
    homepage = "http://proj-clhep.web.cern.ch/proj-clhep/"
    git      = "https://github.com/cms-externals/clhep.git"

    tags = ['hep']

    maintainers = ['drbenmorgan']
    
    generator = 'Ninja'

    version('2.4.5.1.cms', commit='f256fe37039681f7856f0e324ccf9337cdc35b51')

    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    conflicts('cxxstd=17', when='@:2.3.4.2')

    depends_on('cmake@2.8.12.2:', when='@2.2.0.4:2.3.0.0', type='build')
    depends_on('cmake@3.2:', when='@2.3.0.1:', type='build')

    # -- CMS begin: all these changes are in CMS fork
    # root_cmakelists_dir = 'CLHEP'  # Extra directory layer. 

    # def patch(self):
    #     filter_file('SET CMP0042 OLD',
    #                 'SET CMP0042 NEW',
    #                 '%s/CLHEP/CMakeLists.txt' % self.stage.source_path)
    # -- CMS end

    def cmake_args(self):
        cmake_args = ['-DCLHEP_BUILD_CXXSTD=-std=c++{0}'.format(
                      self.spec.variants['cxxstd'].value)]
        return cmake_args
