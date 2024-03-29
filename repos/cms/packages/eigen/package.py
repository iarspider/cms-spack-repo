# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Eigen(CMakePackage):
    """Eigen is a C++ template library for linear algebra matrices,
    vectors, numerical solvers, and related algorithms.
    """

    homepage = 'http://eigen.tuxfamily.org/'
    git = 'https://github.com/cms-externals/eigen-git-mirror.git'
    maintainers = ['HaoZeke']

    version('3.4.90', commit='43d8892d117e4e76b6c472b942ebefee00bfc172')

    # From http://eigen.tuxfamily.org/index.php?title=Main_Page#Requirements
    # "Eigen doesn't have any dependencies other than the C++ standard
    # library."
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo'))

    # TODO: latex and doxygen needed to produce docs with make doc
    # TODO: Other dependencies might be needed to test this package
    def cmake_args(self):
        return ['-DBUILD_TESTING=OFF']

    def setup_run_environment(self, env):
        env.prepend_path('CPATH', self.prefix.include.eigen3)

    @property
    def headers(self):
        headers = find_all_headers(self.prefix.include)
        headers.directories = [self.prefix.include.eigen3]
        return headers
