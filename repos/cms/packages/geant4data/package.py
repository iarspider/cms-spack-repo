# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Geant4data(BundlePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    # There is no URL since there is no code to download.
    phases = ['install']

    version('10.0')

    depends_on("g4ndl")
    depends_on("g4emlow")
    depends_on("g4photonevaporation")
    depends_on("g4radioactivedecay")
    depends_on("g4particlexs")
    depends_on("g4saiddata")
    depends_on("g4abla")
    depends_on("g4ensdfstate")
    depends_on("g4realsurface")
    depends_on("g4incl")

    def install(self, spec, prefix):
        mkdirp(prefix.etc.join('scram.d'))
        with open(prefix.etc.join(join_path('scram.d', 'geant4data.xml')), 'w') as f:
            f.write(f'<tool name="geant4data" version="{spec.version}">\n')
            f.write(' <client>\n')
            f.write(f'    <environment name="GEANT4DATA_BASE" default="{prefix}"/>\n')
            f.write(' </client>\n')

            for dep in spec.dependencies():
                uctool = dep.name.upper()
                toolbase = dep.prefix
                toolver = dep.version
                f.write(f'  <runtime name=\"{uctool}_RUNTIME\" value=\"{toolbase}/share/data/{uctool}{toolver}\" type=\"path\"/>\n')

            f.write('</tool>')

        mkdirp(prefix.etc.join('profile.d'))

        with open(prefix.etc.join(join_path('profile.d', 'init.sh')), 'w') as f:
            f.write(f'GEANT4DATA_ROOT={prefix}\n')
            f.write(f'GEANT4DATA_VERSION={spec.version}\n')

        with open(prefix.etc.join(join_path('profile.d', 'init.csh')), 'w') as f:
            f.write(f'set GEANT4DATA_ROOT {prefix}\n')
            f.write(f'set GEANT4DATA_VERSION {spec.version}\n')

    def setup_run_environment(self, env):
        env.set('GEANT4DATA_ROOT', str(self.spec.prefix))
        env.set('GEANT4DATA_VERSION', str(self.spec.version))
