# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import spack.user_environment as uenv
from spack import *
from spack.util.environment import *


class CmsGeant4data(BundlePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    # There is no URL since there is no code to download.
    phases = ["install"]

    version("10.0")

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

    def get_g4_environment(self, spec):
        with spack.store.db.read_transaction():
            specs = [dep for dep in spec.traverse(order="post")]

        env_mod = spack.util.environment.EnvironmentModifications()

        for _spec in specs:
            env_mod.extend(uenv.environment_modifications_for_spec(_spec))
            env_mod.prepend_path(uenv.spack_loaded_hashes_var, _spec.dag_hash())

        modifications = env_mod.group_by_name()
        new_env = {}
        env_set_not_prepend = {}

        for name, actions in sorted(modifications.items()):
            if not name.startswith("G4"):
                continue
            env_set_not_prepend[name] = False
            for x in actions:
                env_set_not_prepend[name] = env_set_not_prepend[name] or isinstance(
                    x, (SetPath, SetEnv)
                )
                # set a dictionary with the environment variables
                x.execute(new_env)
            if env_set_not_prepend[name] and len(actions) > 1:
                tty.warn("Var " + name + "is set multiple times!")

        return new_env

    def install(self, spec, prefix):
        mkdirp(prefix.etc.join("scram.d"))
        with open(prefix.etc.join(join_path("scram.d", "geant4data.xml")), "w") as f:
            f.write(f'<tool name="geant4data" version="{spec.version}">\n')
            f.write(" <client>\n")
            f.write(f'    <environment name="GEANT4DATA_BASE" default="{prefix}"/>\n')
            f.write(" </client>\n")

            g4env = self.get_g4_environment(spec)

            for k, v in g4env.items():
                f.write(f'  <runtime name="{k}" value="{v}" type="path"/>\n')

            f.write("</tool>")

        mkdirp(prefix.etc.join("profile.d"))

        with open(prefix.etc.join(join_path("profile.d", "init.sh")), "w") as f:
            f.write(f"GEANT4DATA_ROOT={prefix}\n")
            f.write(f"GEANT4DATA_VERSION={spec.version}\n")

        with open(prefix.etc.join(join_path("profile.d", "init.csh")), "w") as f:
            f.write(f"set GEANT4DATA_ROOT {prefix}\n")
            f.write(f"set GEANT4DATA_VERSION {spec.version}\n")

    def setup_run_environment(self, env):
        env.set("GEANT4DATA_ROOT", str(self.spec.prefix))
        env.set("GEANT4DATA_VERSION", str(self.spec.version))
