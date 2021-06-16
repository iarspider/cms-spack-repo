from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../ToolfilePackage'))
from scrampackage import write_scram_toolfile


class PacparserToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../ToolfilePackage/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('pacparser')

    def install(self,spec,prefix):
        values = {}
        values['VER'] = spec['pacparser'].version
        values['PFX'] = spec['pacparser'].prefix
        fname = 'pacparser.xml'
        contents = str("""<tool name="pacparser" version="$VER">
  <info url="http://code.google.com/p/pacparser/"/>
  <lib name="pacparser"/>
  <client>
    <environment name="PACPARSER_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$$PCRE_BASE/lib"/>
    <environment name="INCLUDE" default="$$PCRE_BASE/include"/>
  </client>
  <runtime name="PATH" value="$PACPARSER_BASE/bin" type="path"/> 
  <runtime name="ROOT_INCLUDE_PATH" value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)
