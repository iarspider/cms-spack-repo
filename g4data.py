from llnl.util.filesystem import *

from spack.package import PackageBase, run_after

import re


class G4DataPackage(PackageBase):
    phases = ['setup', 'install']

    def __init__(self, spec):
        super().__init__(spec)
        self.g4dataname = ''
        self.g4datatool = None

        self.build_system_class = 'G4DataPackage'

    @property
    def build_directory(self):
        """Returns the directory containing the main Makefile

        :return: build directory
        """
        return self.stage.source_path

    def setup(self, spec, prefix):
        self.g4datatool = re.sub('^geant4-', '', self.g4dataname)
        self.basetool = self.g4dataname.upper().replace('-', '_')
        self.g4runtime = self.g4runtime or self.g4datatool

    def install(self, spec, prefix):
        mkdirp(self.prefix.data)
        install_tree('.', self.prefix.data)

        self.post_(spec, prefix)

    def post_(self, spec, prefix):
        mkdirp(join_path(self.prefix.etc, 'profile.d'))

        with open(join_path(self.prefix.etc, 'profile.d', 'init.sh'), 'w') as f:
            f.write(self.basetool + "_ROOT='" + prefix + "'" + '\n')
            f.write(self.basetool + "_RUNTIME='" + self.g4runtime+"'" + '\n')
            f.write(self.g4runtime + "='" + join_path(prefix.data, self.g4datatool + str(self.version)) + "'" + '\n')

        with open(join_path(self.prefix.etc, 'profile.d', 'init.csh'), 'w') as f:
            f.write('set ' + self.basetool + "_ROOT='" + prefix + "'" + '\n')
            f.write('set ' + self.basetool + "_RUNTIME='" + self.g4runtime+"'" + '\n')
            f.write('set ' + self.g4runtime + "='" + join_path(prefix.data, self.g4datatool + str(self.version)) + "'" + '\n')

        return

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
