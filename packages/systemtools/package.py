from spack import *
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '../ToolfilePackage'))
from scrampackage import write_scram_toolfile


class Systemtools(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../ToolfilePackage/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('openssl')

    def install(self,spec,prefix):
        # Sockets
        values = {}
        fname = 'sockets.xml'
        contents = str("""<tool name="sockets" version="1.0">$foo</tool>""")
        if spec.satisfies('platform=darwin'):
            values['foo'] = '<lib name="dl"/>'
        elif spec.satisfies('platform=linux'):
            values['foo'] = '<lib name="nsl"/><lib name="crypt"/><lib name="dl"/><lib name="rt"/>'
        else:
            values['foo'] = ''

        write_scram_toolfile(contents, values, fname, prefix)

        # OpenGL
        values = {}
        fname = 'opengl.xml'
        contents = str("""<tool name="opengl" version="XFree4.2">
            <lib name="GL"/>
            <lib name="GLU"/>
            <use name="x11"/>
            <environment name="ORACLE_ADMINDIR" default="${ORACLE_ENV_ROOT}/etc"/>
        </tool>""")

        values['ORACLE_ENV_ROOT'] = os.environ.get('ORACLE_ENV_ROOT', '')
        if spec.satisfies('platform=darwin'):
            values['foo'] = """<client>
      <environment name="OPENGL_BASE" default="/System/Library/Frameworks/OpenGL.framework/Versions/A"/>
      <environment name="INCLUDE"     default="$OPENGL_BASE/Headers"/>
      <environment name="LIBDIR"      default="$OPENGL_BASE/Libraries"/>
    </client>"""
        else:
            values['foo'] = ''

        write_scram_toolfile(contents, values, fname, prefix)

        # OpenSSL
        # NB: built with Spack, not taken from system
        fname = 'openssl.xml'
        values = {}
        values['VER'] = spec['openssl'].version
        values['PFX'] = spec['opessl'].prefix

        contents = str("""<tool name="openssl" version="$VER">
    <lib name="ssl"/>
    <lib name="crypto"/>
    <client>
      <environment name="OPENSSL_BASE" default="$PFX"/>
      <environment name="LIBDIR" default="$$OPENSSL_BASE/lib"/>
      <environment name="INCLUDE" default="$$OPENSSL_BASE/include"/>
    </client>
  </tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

        # X11
        fname = 'x11.xml'
        values = {'foo': ''}
        contents = str("""<tool name="x11" version="R6">$foo<use name="sockets"/></tool>""")
        if self.spec.satisfies('platform=darwin'):
            values['foo'] = """    <client>
      <environment name="INCLUDE" value="/usr/X11R6/include"/>
      <environment name="LIBDIR" value="/usr/X11R6/lib"/>
    </client>
    <runtime name="DYLD_FALLBACK_LIBRARY_PATH" value="$LIBDIR" type="path"/>
    <lib name="Xt"/>
    <lib name="Xpm"/>
    <lib name="X11"/>
    <lib name="Xi"/>
    <lib name="Xext"/>
    <lib name="Xmu"/>
    <lib name="ICE"/>
    <lib name="SM"/> """
        else:
            values['foo'] = ''

        write_scram_toolfile(contents, values, fname, prefix)