# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import shutil


class Hls(Package):
    """HLS_arbitrary_Precision_Types"""

    homepage = "https://www.example.com"
    git = "https://github.com/Xilinx/HLS_arbitrary_Precision_Types.git"

    version('2019.08', commit='200a9aecaadf471592558540dc5a88256cbf880f')

    def install(self, spec, prefix):
        with working_dir('examples/ap_fixed'):
            make()
            shutil.move('a.out', '../ap_fixed.exe')
        shutil.rmtree('examples/ap_fixed')

        with working_dir('examples/ap_int'):
            make()
            shutil.move('a.out', '../ap_int.exe')
        shutil.rmtree('examples/ap_int')

        install_tree('.', prefix)
