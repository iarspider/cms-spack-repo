from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../ToolfilePackage'))
from scrampackage import write_scram_toolfile

class PythonToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../ToolfilePackage/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('python')

    def install(self, spec, prefix):
        pyvers=str(self.spec['python'].version).split('.')
        pyver=pyvers[0]+'.'+pyvers[1]
        values={}
        values['VER']=spec['python'].version
        values['PFX']=spec['python'].prefix
        values['PYVER']=pyver
        fname='python.xml'
        contents = str("""<tool name="python3" version="$VER">
  <lib name="python${PYVER}"/>
  <client>
    <environment name="PYTHON3_BASE" default="$PFX"/>
    <environment name="LIBDIR" default="$PFX/lib"/>
    <environment name="INCLUDE" default="$PFX/include/python${PYVER}"/>
    <environment name="PYTHON3_COMPILE" default="$PFX/lib/python${PYVER}/compileall.py"/>
  </client>
  <runtime name="PATH" value="$PFX/bin" type="path"/>
  <use name="sockets"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)
