# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import shutil

from spack import *


class Dqmgui(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.example.com"
    git = "https://github.com/cms-DQM/dqmgui.git"

    version("1.0.1", tag="1.0.1")

    depends_on("root")
    depends_on("boost")
    depends_on("python@3:")

    depends_on("py-aiohttp", type=("build", "run"))
    depends_on("py-aiosqlite", type=("build", "run"))
    depends_on("py-async-lru", type=("build", "run"))
    depends_on("py-contextvars", type=("build", "run"))

    def install(self, spec, prefix):
        shutil.rmtree(join_path(self.stage.source_path, "objs"))
        shutil.rmtree(join_path(self.stage.source_path, "src"))
        shutil.rmtree(join_path(self.stage.source_path, "plugins"))
        install_tree(".", prefix)
