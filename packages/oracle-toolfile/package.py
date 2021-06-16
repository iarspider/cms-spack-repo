from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../ToolfilePackage'))
from scrampackage import write_scram_toolfile


class OracleToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../ToolfilePackage/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('oracle-instant-client')

    def install(self, spec, prefix):
        values = {}
        values['VER'] = spec['oracle-instant-client'].version
        values['PFX'] = spec['oracle-instant-client'].prefix
        fname = 'oracle.xml'
        contents = str("""<tool name="oracle" version="$VER">
  <lib name="clntsh"/>
  <client>
    <environment name="ORACLE_BASE" default="$PFX"/>
    <environment name="ORACLE_ADMINDIR" value="$PFX/etc"/>
    <environment name="LIBDIR" value="$$ORACLE_BASE/lib"/>
    <environment name="BINDIR" value="$$ORACLE_BASE/bin"/>
    <environment name="INCLUDE" value="$$ORACLE_BASE/include"/>
  </client>
  <runtime name="PATH" value="$$BINDIR" type="path"/>
  <runtime name="TNS_ADMIN" default="$$ORACLE_ADMINDIR"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
  <use name="sockets"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'oracleocci.xml'
        contents = str("""<tool name="oracleocci-official" version="$VER">
  <lib name="occi"/>
  <use name="oracle"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)
