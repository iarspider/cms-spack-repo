# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import glob
import os
import re

class CrabDev(Package):
    """crab-dev"""

    homepage = "https://www.example.com"
    url = "file://" + os.path.dirname(__file__) + '/junk.xml'

    # wmcore_version = '1.5.3'
    crab_client_version = 'v3.221004'
    crab_client_revision = '00'
    crab_server_version = 'v3.221003'
    dbs_version = '3.14.0'
    thisdir = os.path.dirname(__file__)

    resource(
        name='CRABClient',
        git='https://github.com/dmwm/CRABClient.git',
        tag=crab_client_version,
        destination='.'
    )
    #resource(
    #    name='WMCore',
    #    git='https://github.com/dmwm/WMCore.git',
    #    tag=wmcore_version,
    #    destination='.'
    #)
    resource(
        name='CRABServer',
        git='https://github.com/dmwm/CRABServer.git',
        tag=crab_server_version,
        destination='.'
    )
    resource(
        name='DBS',
        git='https://github.com/dmwm/DBS.git',
        tag=dbs_version,
        destination='.'
    )

    version(crab_client_version + '.' + crab_client_revision, sha256='af147dd4a6c715dde7e0f13f4fb990029c13833d73fffc281a09709ce422c46b', expand=False)

    # wmcore_packages = ("PSetTweaks", "Utils", "WMCore")
    crabserver_packages = ("ServerUtilities.py", )
    dbs_packages = ("Client/src/python/dbs", "PycurlClient/src/python/RestClient")

    def install(self, spec, prefix):
        crab_type = os.path.basename(os.path.dirname(__file__)).replace('crab-', '')
        #Copy CRABClient
        install_tree(join_path('CRABClient', 'src', 'python'), prefix.lib)
        filter_file('"development"', '"{0}"'.format(self.spec.version), prefix.lib.CRABClient.join("__init__.py"))
        install_tree(join_path('CRABClient', 'bin'), prefix.bin)
        install_tree(join_path('CRABClient', 'etc'), prefix.etc)

        #List of CRAB python pakcages for which we need to create ProxyPackage symlink
        with open(prefix.etc.join('crab_py_pkgs.txt'), 'w') as f:
            for fn in glob.glob('CRABClient/src/python/*/__init__.py'):
                f.write(os.path.dirname(fn) + "\n")
            f.write('dbs\n')
            f.write('RestClient\n')

        #Create fake WMCore
        mkdirp(prefix.lib.WMCore)
        install('CRABClient/src/python/CRABClient/WMCoreConfiguration.py', prefix.lib.WMCore)
        touch(prefix.lib.WMCore.join('__init__.py'))

        #Copy CRABServer
        for pkg in self.crabserver_packages:
            if os.path.isfile("CRABServer/src/python/" + pkg):
                install("CRABServer/src/python/" + pkg, prefix.lib)
            else:
                install_tree("CRABServer/src/python/" + pkg, prefix.lib.join(pkg))

        #Copy DBS
        for pkg in self.dbs_packages:
            if os.path.isfile("DBS/" + pkg):
                install("DBS/" + pkg, prefix.lib)
            else:
                install_tree("DBS/" + pkg, prefix.lib.join(pkg))
        install_tree("DBS/Client/utils", prefix.examples)

        flags = [False, False]
        with open(prefix.etc.join('crab-bash-completion.sh')) as f:
            for line in f:
                if '_UseCrab' in line:
                    flags[0] = True
                if re.search(' filenames  *crab', line):
                    flags[1] = True

        if all(flags):
            filter_file('_UseCrab', '_UseCrab_' + crab_type, prefix.etc.join('crab-bash-completion.sh'))
            filter_file(' filenames  *crab', ' filenames crab-' + crab_type, prefix.etc.join('crab-bash-completion.sh'))
            if crab_type == 'prod':
                with open(prefix.etc.join('crab-bash-completion.sh'), 'a') as f:
                    f.write("complete -F _UseCrab_prod -o filenames crab\n")
        else:
            raise RuntimeError("ERROR: Unable to fix crab use function _UseCrab")
        install(join_path(self.thisdir, 'cmspost.sh'), prefix)
        filter_file('%{ver}', str(spec.version), join_path(prefix, 'cmspost.sh'))
        set_executable(join_path(prefix, 'cmspost.sh'))

