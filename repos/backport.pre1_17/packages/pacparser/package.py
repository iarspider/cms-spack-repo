# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pacparser(MakefilePackage):
    """pacparser is a library to parse proxy auto-config (PAC) files."""

    homepage = "http://pacparser.github.io/"
    url      = "https://github.com/manugarg/pacparser/releases/download/1.3.7/pacparser-1.3.7.tar.gz"

    version('1.3.7', sha256='eb48ec2fc202d12a4b882133048c7590329849f32c2285bc4dbe418f29aad249')
    version('1.3.5', sha256='685febe519c8fd26c4a21d8e56e318839d82cab37bd81d74f2c5b8a3544f1a81')

    depends_on('python', when='+python')
    depends_on('py-setuptools', when='+python', type=('build', 'run'))

    variant('python', default=False,
            description='Build and install python bindings')

    def build(self, spec, prefix):
        make('-C', 'src', parallel=False)
        if '+python' in spec:
            make('-C', 'src', 'pymod', parallel=False)

    def install(self, spec, prefix):
        make('-C', 'src', 'install', 'PREFIX=' + self.prefix)
        if '+python' in spec:
            make('-C', 'src', 'install-pymod', 'PREFIX=' + self.prefix,
                 'EXTRA_ARGS=--prefix={0}'.format(prefix))
