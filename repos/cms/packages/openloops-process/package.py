# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


def local_file(fn):
    return join_path(os.path.dirname(__file__), fn)


def local_file_url(fn):
    return "file://" + local_file(fn)


# HACK!
class OpenloopsProcess(Package):
    """Download process sources for OpenLoops"""

    homepage = "https://github.com/cms-externals/openloops"
    git = "https://github.com/cms-externals/openloops.git"

    #    version('2.1.2', branch='cms/v2.1.2')
    version(
        "2.1.2",
        url="https://cmsrep.cern.ch/cmssw/repos/cms/SOURCES/slc7_amd64_gcc10/external/openloops-process/2.1.2/process_src.tgz",
        sha256="c12bfe172cfd0ef55d14ef4b9f6f40410eccdbc592de29e6c0da17e65a589569",
    )
    #    patch('openloops-urlopen2curl.patch')

    resource(
        name="cms.coll",
        url=local_file_url("cms.coll"),
        sha256="ad84441b47bc01ea74487d153943d6bf9c6f2a1c40e6c158f9d0ce886ef29e4b",
        when="~tiny",
        expand=False,
        placement={"cms.coll": "cms.coll"},
    )

    resource(
        name="tiny.coll",
        url=local_file_url("tiny.coll"),
        sha256="aad91817040d29202ca87c829aa12e4129d8b28c8dee5ebfff4ef415192e7163",
        when="+tiny",
        expand=False,
        placement={"tiny.coll": "tiny.coll"},
    )

    variant(
        "tiny",
        default=False,
        description="Only download one process to speed things up",
    )

    depends_on("python@2.7,3.2:", type="build")

    def install(self, spec, prefix):
        # coll_file = 'cms.coll' if not self.spec.variants['tiny'].value else 'tiny.coll'
        # if self.spec.satisfies('target=aarch64:'):
        #     filter_file('pplljj_ew', '', coll_file)

        # copy(join_path(os.path.dirname(__file__), coll_file), coll_file)
        # downloader = Executable('./pyol/bin/download_process.py')
        # downloader(coll_file)
        install_tree("process_src", self.prefix.process_src)
        install_tree("proclib", self.prefix.proclib)
        if self.spec.satisfies("~tiny"):
            install(local_file("cms.coll"), self.prefix)
        else:
            install(local_file("tiny.coll"), self.prefix)
