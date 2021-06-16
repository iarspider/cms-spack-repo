from spack import *
import sys,os

class FrontierClient(MakefilePackage):
    url      = "https://github.com/fermitools/frontier/archive/v2_9_1.tar.gz"

    version('2_9_1',  sha256='d21370fbe142807966e3c2218ce361ea3bb573498e1b8387b801fb6641c3ed22')
    version('2_9_0',  sha256='e58dba3f177c5b74609f244101a22a5c14d42bf019013fe2dba72c09f819c62a')
    version('2_8_21', sha256='7df9ba61c3e1778aca75c5da6e45ee4d00b5c061d3f7162208e2fbd2ec266a9e')
    version('2_8_20', sha256='81b0f45762d96a33f156e0238631a60eef910a176644e95c6c19a36824bef7e1')

    patch('frontier_client-2.8.20-add-python-dbapi.patch')

    depends_on('openssl')
    depends_on('expat')
    depends_on('zlib')
    depends_on('pacparser')
    depends_on('python')

    def build(self, spec, prefix):
        make('-j1', 'EXPAT_DIR=%s' % spec['expat'].prefix,
             'PACPARSER_DIR=%s' % spec['pacparser'].prefix,
             'COMPILER_TAG=gcc_%s' % spec.compiler.version,
             'ZLIB_DIR=%s' % spec['zlib'].prefix,
             'OPENSSL_DIR=%s' % spec['openssl'].prefix,
             'CXXFLAGS=-ldl', 'CFLAGS=-I%s' % spec['openssl'].prefix.include,
             'all'
             )

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        make('-j1', 'EXPAT_DIR=%s' % spec['expat'].prefix,
             'PACPARSER_DIR=%s' % spec['pacparser'].prefix,
             'COMPILER_TAG=gcc_%s' % spec.compiler.version,
             'ZLIB_DIR=%s' % spec['zlib'].prefix,
             'OPENSSL_DIR=%s' % spec['openssl'].prefix,
             'CXXFLAGS=-ldl',
             'distdir=%s' % prefix,
             'dist'
             )
        install_tree('python', prefix + '/python')
