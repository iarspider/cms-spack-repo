from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../ToolfilePackage'))
from scrampackage import write_scram_toolfile


class UuidToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../ToolfilePackage/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    if sys.platform == 'darwin':
      depends_on('libuuid')
    else:
      depends_on('util-linux-uuid')

    def install(self, spec, prefix):
        values = {}
        if sys.platform == 'darwin':
          values['VER'] = spec['libuuid'].version
          values['PFX'] = spec['libuuid'].prefix
        else:
          values['VER'] = spec['util-linux-uuid'].version
          values['PFX'] = spec['util-linux-uuid'].prefix
        fname = 'uuid-cms.xml'
        contents = str("""<tool name="libuuid" version="$VER">
  <lib name="uuid"/>
  <client>
    <environment name="LIBUUID_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$LIBUUID_BASE/lib"/>
    <environment name="INCLUDE" default="$$LIBUUID_BASE/include"/>
  </client>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)
