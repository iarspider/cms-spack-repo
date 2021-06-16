from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../ToolfilePackage'))
from scrampackage import write_scram_toolfile


class ZstdToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../ToolfilePackage/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('zstd')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = self.spec['zstd'].version
        values['PFX'] = self.spec['zstd'].prefix
        fname = 'zstd.xml'
        contents = str("""<tool name="zstd" version="$VER">
  <lib name="zstd"/>
  <client>
    <environment name="ZSTD_BASE" default="$PFX"/>
    <environment name="INCLUDE" default="$$ZLIB_BASE/include"/>
    <environment name="LIBDIR" default="$$ZLIB_BASE/lib"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
""")
        write_scram_toolfile(contents, values, fname, prefix)
