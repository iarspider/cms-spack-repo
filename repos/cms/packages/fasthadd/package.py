# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fasthadd(MakefilePackage):
    """FastHADD"""

    homepage = "https://www.example.com"

    commit="905af02d3369428df677c232537da6fca8982ff3"
    version('2.3', url=f"https://raw.githubusercontent.com/cms-sw/cmssw/{commit}/DQMServices/Components/bin/fastHadd.cc", expand=False,
            sha256='e81a8777fa4e281e16aa0c8924ca7ed83558430b46102957c6b38ce7d6f6237f')

    resource(name='protofile',
             url=f'https://raw.githubusercontent.com/cms-sw/cmssw/{commit}/DQMServices/Core/src/ROOTFilePB.proto',
             expand=False,
             sha256='52c020ceec5252b9eb57d88f8c1b535844f7e24704fb0c4741cce84818b4484c',
             destination='.',
             placement={'ROOTFilePB.proto': 'ROOTFilePB.proto'})

    depends_on('root')
    depends_on('protobuf@:3.6.10')
    phases = ['install']

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.etc.join('profile.d'))
        protoc = which('protoc', required=True)
        protoc("-I", "./", "--cpp_out=./", "ROOTFilePB.proto")
        filter_file('DQMServices/Core/src/', '', 'ROOTFilePB.pb.cc')
        filter_file('DQMServices/Core/src/', '', 'fastHadd.cc')

        root_config = which('root-config', required=True)
        root_flags = root_config('--cflags', '--libs', output=str).split()

        flags = ["-O2", "-o", prefix.bin.fastHadd, "ROOTFilePB.pb.cc", "./fastHadd.cc", "-I" + self.spec["protobuf"].prefix.include, "-L" + self.spec["protobuf"].prefix.lib, "-lprotobuf"]
        flags.extend(root_flags)
        gcc = Executable(self.compiler.cxx)
        gcc(*flags)
