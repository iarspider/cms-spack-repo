# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import platform
import os
import shutil


def oracleclient_releases():
    releases = [
        {
            'version': '21.1.0.0.0',
            'Linux-x86_64': {
                'basic': ['https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-basic-linux.x64-21.1.0.0.0.zip', '9b63e264c01ac54a0f0e61bd638576aed6f04a36b305bcd17847755e7b9855ce'],
                'sqlplus': ['https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-sqlplus-linux.x64-21.1.0.0.0.zip', '3220f486940e82f1a7825e8f0875729d63abd57cc708f1908e2d5f2163b93937'],
                'tools': ['https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-tools-linux.x64-21.1.0.0.0.zip', 'ff652d5bbfeaaa2403cbc13c5667f52e1d648aa2a5c59a50f4c9f84e6d2bba74'],
                'sdk': ['https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-sdk-linux.x64-21.1.0.0.0.zip', '80a465530a565ed327ab9ae0d9fc067ed42338536c7e8721cf2c26e474f4f75f'],
                'jdbc': ['https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-jdbc-linux.x64-21.1.0.0.0.zip', '76c866272712f2b432cc4be675605b22deca02f7a88a292b5ed8d29212d79dc7'],
                'odbc': ['https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-odbc-linux.x64-21.1.0.0.0.zip', 'ec7722b522684f0a3f63481573d0eb3537764224eabed6223f33699dd940bf20']
            }
        },
        {
            'version': '19.11.0.0.0',
            'Linux-x86_64': {
                'basic': ['https://download.oracle.com/otn_software/linux/instantclient/1911000/instantclient-basic-linux.x64-19.11.0.0.0dbru.zip', 'd3b477b9618ee06ccbc983557597c98fd3085856ccdbe091e86dd9d6b9dcfd2b'],
                'sqlplus': ['https://download.oracle.com/otn_software/linux/instantclient/1911000/instantclient-sqlplus-linux.x64-19.11.0.0.0dbru.zip', '84e528530ede8c00fd24266a51a9a3593e4ca9e87cb86808c99685766e5b10ab'],
                'tools': ['https://download.oracle.com/otn_software/linux/instantclient/1911000/instantclient-tools-linux.x64-19.11.0.0.0dbru.zip', '6a1c4a71b23da3ffb6c93e2ea07e28ecd67790c4b4446cf90524911b9beb2dc2'],
                'sdk': ['https://download.oracle.com/otn_software/linux/instantclient/1911000/instantclient-sdk-linux.x64-19.11.0.0.0dbru.zip', 'e854e7f51e7ca2958153f6c8fee416afa5b3f3baecdfa88ed2ecea2daf012a4a'],
                'jdbc': ['https://download.oracle.com/otn_software/linux/instantclient/1911000/instantclient-jdbc-linux.x64-19.11.0.0.0dbru.zip', '008e907449e7dc0dcf41f8a0d78658bb3dfbdcc996d69f8ddda635456ab3df21'],
                'odbc': ['https://download.oracle.com/otn_software/linux/instantclient/1911000/instantclient-odbc-linux.x64-19.11.0.0.0dbru.zip', '0a16d0ccae54fccec830a1137c6566b4569448c655435b9e6b656fcae69e716b']
            }
        },
        {
            'version': '19.10.0.0.0',
            'Linux-x86_64': {
                'basic': ['https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-basic-linux.x64-19.10.0.0.0dbru.zip', 'c2eeea093d70f5416f8a8560f9fa5b57707a76ac9775906dbc4aaa778fdee84f'],
                'sqlplus': ['https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-sqlplus-linux.x64-19.10.0.0.0dbru.zip', 'eee44825f348966796166beb8c0d8cc8f61929bae05229b65b34794e0f05659a'],
                'tools': ['https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-tools-linux.x64-19.10.0.0.0dbru.zip', '93bf58d2e15bb3ca98f8e5f579a93760571a37e0d9312187f6a5f228d492c863'],
                'sdk': ['https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-sdk-linux.x64-19.10.0.0.0dbru.zip', '2c4ae1b77fe32f3d3bf86a4ef560dc3a5dcbf5d11d742b4afeca414e5388ff2f'],
                'jdbc': ['https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-jdbc-linux.x64-19.10.0.0.0dbru.zip', '3fabbc4a86b8c5b4b29c4d76524c7d7e5bfab33cdbfa73f1199fc5582ed25df6'],
                'odbc': ['https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-odbc-linux.x64-19.10.0.0.0dbru.zip', '1c7ae3ea5913af9647ae68e2053cdaf9154ef6c9aa07e8b7d91e1ead9d5e675a']
            },
            'Linux-aarch64': {
                'basic': ['https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-basic-linux.arm64-19.10.0.0.0dbru.zip', '0cd9ed1f6d01026a3990ecfbb84816d8d5da35fc1dbc9f25f28327a79d013ac6'],
                'sqlplus': ['https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-sqlplus-linux.arm64-19.10.0.0.0dbru.zip', '8877328a31e102f8ec02a37d47e471a36478ee4f78d15bcf6d271cd8c5989f44'],
                'tools': ['https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-tools-linux.arm64-19.10.0.0.0dbru.zip', 'e1063413072772dc0f9ba6460d92ee74e14ce14c9c2c5991225b8a1975704743'],
                'sdk': ['https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-sdk-linux.arm64-19.10.0.0.0dbru.zip', 'f15a643722f214c51f4306d9a520d5fc207de51a177da32bf30e7c711b7fb32c'],
                'jdbc': ['https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-jdbc-linux.arm64-19.10.0.0.0dbru.zip', 'ce16c3cc75ed7c5da13248912d51b7b8fc5a6f90d8b0b52c4bd3c19058264ede'],
                'odbc': ['https://download.oracle.com/otn_software/linux/instantclient/191000/instantclient-odbc-linux.arm64-19.10.0.0.0dbru.zip', '4fe44820acd9f71120fc4ef6a5fb39c6a1f3d96b8858ac7fa117c3ad06f0de6b']
            }
        },
        {
            'version': '19.3.0.0.0',
            'Linux-ppc64le': {
                'basic': ['https://download.oracle.com/otn_software/linux/instantclient/193/instantclient-basic-linux.leppc64.c64-19.3.0.0.0dbru.zip', '4345cea0f6f4c9d7a1f8fca78941d6e3e3b3fdb877928d34f3951d49a2fdda6e'],
                'sqlplus': ['https://download.oracle.com/otn_software/linux/instantclient/193/instantclient-sqlplus-linux.leppc64.c64-19.3.0.0.0dbru.zip', 'd55daa12fdc00666f507e530188909d637f46a12ae7f82c93afe12d270e359e5'],
                'tools': ['https://download.oracle.com/otn_software/linux/instantclient/193/instantclient-tools-linux.leppc64.c64-19.3.0.0.0dbru.zip', 'ae15a1143ff0630e80e2eee38fbb69918f5dc999abf8e811242823eed46bb5aa'],
                'sdk': ['https://download.oracle.com/otn_software/linux/instantclient/193/instantclient-sdk-linux.leppc64.c64-19.3.0.0.0dbru.zip', 'b09277005d2a17e98b78606e8d5fa57463528a46273f392b4ecede49ebc65ecf'],
                'jdbc': ['https://download.oracle.com/otn_software/linux/instantclient/193/instantclient-jdbc-linux.leppc64.c64-19.3.0.0.0dbru.zip', 'bb05492d5d1c06b74c115f351f543206428ff47f0b9d381c838d54e43db05a73'],
                'odbc': ['https://download.oracle.com/otn_software/linux/instantclient/193/instantclient-odbc-linux.leppc64.c64-19.3.0.0.0dbru.zip', 'b7edd85888ea5b0da2e93b8b1ac80c220749b6b014776fcb29936a098ad478f4']
            }
        }
    ]

    return releases


class OracleInstantClient(Package):
    """Oracle instant client"""

    homepage = "https://www.oracle.com/database/technologies/instant-client.html"
    url      = "https://download.oracle.com/otn_software/linux/instantclient/211000/instantclient-basic-linux.x64-21.1.0.0.0.zip"

    releases = oracleclient_releases()
    key = "{0}-{1}".format(platform.system(), platform.machine()) 
    for release in releases:
        oracle_version = release['version']
        packages = release.get('key', None)
        if packages is None:
            continue
            
        main_pkg = release[key]['basic']
        url, sha256 = main_pkg
        version(oracle_version, sha256=sha256, url=url)
        for rname, atts in release[key].items():
            if rname == 'basic':
                continue
            url, sha256 = atts
            condition = "@{0}".format(oracle_version)
            resource(name=rname, url=url, sha256=sha256, when=condition, placement=rname)
            
        if platform.machine() == 'x86_64':
            # -- CMS: OCCI lib with new C++ ABI (GCC 5 and above)
            resource(name='occi_lib', url='http://cmsrep.cern.ch/cmssw/download/oracle-mirror/x64/libocci.so.19.1.zip', 
                     sha256='f5c9031944a12543f2c61e0f65b00a4cb2b62cd152579679d37c780b93653718',
                     when='@19.3.0.0:19.11.9.9 ', placement='occi_lib')

    depends_on('libaio', type='link')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.include)
        mkdirp(prefix.lib)
        mkdirp(prefix.doc)

        for dirn, fns in {'.': ('adrci', 'genezi', 'uidrvci'),
                          'sqlplus': ('glogin.sql', 'sqlplus'),
                          'odbc': ('odbc_update_ini.sh', ),
                          'tools': ('exp', 'expdp', 'imp', 'impdp', 'sqlldr', 'wrc')
                          }.items():
            for fn in fns:
                install(join_path(dirn, fn), prefix.bin)

        for fn in glob.glob(join_path(self.stage.source_path, '*.so*')):
            install(fn, prefix.lib)

        for fn in glob.glob(join_path(self.stage.source_path, '*.jar')):
            install(fn, prefix.lib)

        for fn in glob.glob(join_path(self.stage.source_path, 'sqlplus', '*.so*')):
            install(fn, prefix.lib)

        for fn in glob.glob(join_path(self.stage.source_path, 'jdbc', '*.so*')):
            install(fn, prefix.lib)

        for fn in glob.glob(join_path(self.stage.source_path, 'odbc', '*.so*')):
            install(fn, prefix.lib)

        for fn in glob.glob(join_path(self.stage.source_path, 'tools', '*.so*')):
            install(fn, prefix.lib)

        for fn in glob.glob(join_path(self.stage.source_path, 'jdbc', '*.jar')):
            install(fn, prefix.lib)

        install_tree('network', prefix.lib)

        for dirn, fns in {'.': ('BASIC_LICENSE', 'BASIC_README'),
                          'sqlplus': ('SQLPLUS_LICENSE', 'SQLPLUS_README'),
                          'jdbc': ('JDBC_LICENSE', 'JDBC_README'),
                          'odbc': ('ODBC_LICENSE', 'ODBC_README'),
                          'sdk': ('SDK_LICENSE', 'SDK_README'),
                          'tools': ('TOOLS_LICENSE', 'TOOLS_README')
                          }.items():
            for fn in fns:
                install(join_path(dirn, fn), prefix.doc)

        install_tree(join_path('odbc', 'help'), prefix.doc)
        install_tree(join_path('sdk', 'sdk', 'include'), prefix.include)
        
        # -- CMS
        if os.path.exists(join_path(prefix.lib, 'libocci_gcc53.so.19.1')):
            shutil.move(join_path(prefix.lib, 'libocci_gcc53.so.19.1'), join_path(prefix.lib, 'libocci.so.19.1'))
