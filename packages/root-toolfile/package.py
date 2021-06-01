from spack import *
import sys,os,re
sys.path.append(os.path.join(os.path.dirname(__file__), '../ToolfilePackage'))
from scrampackage import write_scram_toolfile


class RootToolfile(Package):
    url = 'file://' + os.path.dirname(__file__) + '/../ToolfilePackage/junk.xml'
    version('1.0', '68841b7dcbd130afd7d236afe8fd5b949f017615', expand=False)
    depends_on('root')

    def install(self, spec, prefix):
        gcc = which(spack_f77)
        gcc_prefix = re.sub('/bin/.*$', '', self.compiler.f77)
        gcc_machine = gcc('-dumpmachine', output=str)
        gcc_ver = gcc('-dumpversion', output=str)

        values = {}
        values['VER'] = spec['root'].version
        values['PFX'] = spec['root'].prefix
        values['GCC_VER'] = gcc_ver.rstrip()
        values['GCC_PREFIX'] = gcc_prefix
        values['GCC_MACHINE'] = gcc_machine.rstrip()

        fname = 'root_interface.xml'
        contents = str("""<tool name="root_interface" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <client>
    <environment name="ROOT_INTERFACE_BASE"     default="$PFX"/>
    <environment name="INCLUDE"                 default="$PFX/include"/>
    <environment name="LIBDIR"                  default="$PFX/lib"/>
  </client>
  <runtime name="PATH"                          value="$PFX/bin" type="path"/>
  <runtime name="ROOTSYS"                       value="$PFX/"/>
  <runtime name="ROOT_TTREECACHE_SIZE"          value="0"/>
  <runtime name="ROOT_TTREECACHE_PREFILL"       value="0"/>
  <runtime name="ROOT_INCLUDE_PATH"             value="$$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

        fname = 'root_cxxdefaults.xml'
        if sys.platform == 'darwin':
          contents = str("""<tool name="root_cxxdefaults" version="$VER">
</tool>""")
          write_scram_toolfile(contents, values, fname, prefix)
        else:
          contents = str("""<tool name="root_cxxdefaults" version="$VER">
  <runtime name="ROOT_GCC_TOOLCHAIN" value="$GCC_PREFIX" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/local/include" type="path" handler="warn"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/include" type="path" handler="warn"/>
</tool>""")
          write_scram_toolfile(contents, values, fname, prefix)

# rootcling toolfile
        fname = 'rootcling.xml'
        contents = str("""<tool name="rootcling" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Core"/>
  <flags OVERRIDABLE_FLAGS="ROOTCLING_ARGS"/>
  <use name="root_interface"/>
  <use name="sockets"/>
  <use name="pcre"/>
  <use name="zlib"/>
  <use name="xz"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

# rootrint toolfile
        fname = 'rootrint.xml'
        contents = str("""<tool name="rootrint" version="$VER'">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Rint"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

# rootsmatrix toolfile
        fname = 'rootsmatrix.xml'
        contents = str("""<tool name="rootsmatrix" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Smatrix"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootrio toolfile
        fname = 'rootrio.xml'
        contents = str("""<tool name="rootrio" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RIO"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootthread toolfile
        fname = 'rootthread.xml'
        contents = str("""<tool name="rootthread" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Thread"/>
  <use name="rootrio"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootxmlio toolfile
        fname = 'rootxmlio.xml'
        contents = str("""<tool name="rootxmlio" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="XMLIO"/>
  <use name="rootrio"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootmathcore toolfile
        fname = 'rootmathcore.xml'
        contents = str("""<tool name="rootmathcore" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="MathCore"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootcore toolfile
        fname = 'rootcore.xml'
        contents = str("""<tool name="rootcore" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Tree"/>
  <lib name="Net"/>
  <use name="rootmathcore"/>
  <use name="rootthread"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# roothistmatrix toolfile
        fname = 'roothistmatrix.xml'
        contents = str("""<tool name="roothistmatrix" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Hist"/>
  <lib name="Matrix"/>
  <use name="rootcore"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

# rootdataframe toolfile
        fname = 'rootdataframe.xml'
        contents = str("""<tool name="rootdataframe" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="ROOTDataFrame"/>
  <use name="rootcore"/>
  <use name="rootgraphics"/>
  <use name="roothistmatrix"/>
  <use name="rootrio"/>
  <use name="rootvecops"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

# rootvecops toolfile
        fname = 'rootvecops.xml'
        contents = str("""<tool name="rootvecops" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="ROOTVecOps"/>
  <use name="rootcore"/>
</tool>""")


# rootspectrum toolfile
        fname = 'rootspectrum.xml'
        contents = str("""<tool name="rootspectrum" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Spectrum"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootphysics toolfile
        fname = 'rootphysics.xml'
        contents = str("""<tool name="rootphysics" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Physics"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# root toolfile, alias for rootphysics. Using rootphysics is preferred.
        fname = 'root.xml'
        contents = str("""<tool name="root" version="$VER">
  <info url="http://root.cern.ch/root/"/>a
  <use name="rootphysics"/>
  <flags GENREFLEX_FAILES_ON_WARNS="--fail_on_warnings"/>
  <flags CXXMODULES="0"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootgpad toolfile
        fname = 'rootgpad.xml'
        contents = str("""<tool name="rootgpad" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Gpad"/>
  <lib name="Graf"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootgraphics toolfile, identical to old "root" toolfile
        fname = 'rootgraphics.xml'
        contents = str("""<tool name="rootgraphics" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="TreePlayer"/>
  <lib name="Graf3d"/>
  <lib name="Postscript"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rooteg toolfile, identical to old "root" toolfile
        fname = 'rooteg.xml'
        contents = str("""<tool name="rooteg" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="EG"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootpy toolfile, identical to old "root" toolfile
        fname = 'rootpy.xml'
        contents = str("""<tool name="rootpy" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootinteractive toolfile
        fname = 'rootinteractive.xml'
        contents = str("""<tool name="rootinteractive" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Gui"/>
  <use name="libjpeg-turbo"/>
  <use name="libpng"/>
  <use name="rootgpad"/>
  <use name="rootrint"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootmath toolfile
        fname = 'rootmath.xml'
        contents = str("""<tool name="rootmath" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GenVector"/>
  <lib name="MathMore"/>
  <use name="rootcore"/>
  <use name="gsl"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootminuit toolfile
        fname = 'rootminuit.xml'
        contents = str("""<tool name="rootminuit" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Minuit"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootminuit2 toolfile
        fname = 'rootminuit2.xml'
        contents = str("""<tool name="rootminuit2" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Minuit2"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootrflx toolfile
        fname = 'rootrflx.xml'
        contents = str("""<tool name="rootrflx" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <client>
    <environment name="ROOTRFLX_BASE" default="$PFX"/>
  </client>
  <flags GENREFLEX_GCCXMLOPT="-m64"/>
  <flags GENREFLEX_CPPFLAGS="-DCMS_DICT_IMPL -D_REENTRANT -DGNUSOURCE -D__STRICT_ANSI__"/>
  <runtime name="GENREFLEX" value="$PFX/bin/genreflex"/>
  <use name="root_interface"/>
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# roothtml toolfile
        fname = 'roothtml.xml'
        contents = str("""<tool name="roothtml" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Html"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootmlp toolfile
        fname = 'rootmlp.xml'
        contents = str("""<tool name="rootmlp" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="MLP"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# roottmva toolfile
        fname = 'roottmva.xml'
        contents = str("""<tool name="roottmva" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="TMVA"/>
  <use name="rootmlp"/>
  <use name="rootminuit"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootpymva toolfile
        fname = 'rootpymva.xml'
        contents = str("""<tool name="rootpymva" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="PyMVA"/>
  <use name="roottmva"/>
  <use name="numpy-c-api"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootxml toolfile
        fname = 'rootxml.xml'
        contents = str("""<tool name="rootxml" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="XMLParser"/>
  <use name="rootcore"/>
  <use name="libxml2"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootfoam toolfile
        fname = 'rootfoam.xml'
        contents = str("""<tool name="rootfoam" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Foam"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootgeom toolfile
        fname = 'rootgeom.xml'
        contents = str("""<tool name="rootgeom" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Geom"/>
  <use name="rootrio"/>
  <use name="rootmathcore"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootgeompainter toolfile
        fname = 'rootgeompainter.xml'
        contents = str("""<tool name="rootgeompainter" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GeomPainter"/>
  <use name="rootgeom"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootrgl toolfile
        fname = 'rootrgl.xml'
        contents = str("""<tool name="rootrgl" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RGL"/>
  <use name="rootglew"/>
  <use name="rootgui"/>
  <use name="rootinteractive"/>
  <use name="rootgraphics"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rooteve toolfile
        fname = 'rooteve.xml'
        contents = str("""<tool name="rooteve" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Eve"/>
  <use name="rootgeompainter"/>
  <use name="rootrgl"/>
  <use name="rootged"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# rootguihtml toolfile
        fname = 'rootguihtml.xml'
        contents = str("""<tool name="rootguihtml" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GuiHtml"/>
  <use name="rootgui"/>
  <use name="rootinteractive"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# roofitcore toolfile
        fname = 'roofitcore.xml'
        contents = str("""<tool name="roofitcore" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFitCore"/>
  <client>
    <environment name="ROOFIT_BASE" default="$$TOOL_ROOT"/>
  </client>
  <runtime name="ROOFITSYS" value="$$ROOFIT_BASE/"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
  <use name="rootminuit"/>
  <use name="root_cxxdefaults"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# roofit toolfile
        fname = 'roofit.xml'
        contents = str("""<tool name="roofit" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFit"/>
  <use name="roofitcore"/>
  <use name="rootcore"/>
  <use name="rootmath"/>
  <use name="roothistmatrix"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# roostats toolfile
        fname = 'roostats.xml'
        contents = str("""<tool name="roostats" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooStats"/>
  <use name="roofitcore"/>
  <use name="roofit"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)


# histfactory toolfile
        fname = 'histfactory.xml'
        contents = str("""<tool name="histfactory" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="HistFactory"/>
  <use name="roofitcore"/>
  <use name="roofit"/>
  <use name="roostats"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
  <use name="rootxml"/>
  <use name="rootfoam"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

#Root Ged
        fname = 'rootged.xml'
        contents = str("""<tool name="rootged" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Ged"/>
  <use name="rootgui"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

#Root GLEW
        fname = 'rootglew.xml'
        contents = str("""<tool name="rootglew" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GLEW"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

#Root Gui
        fname = 'rootgui.xml'
        contents = str("""<tool name="rootgui" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Gui"/>
  <use name="rootgpad"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

# ROOT imt
        fname = 'rootimt.xml'
        contents = str("""<tool name="rootimt" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Imt"/>
  <use name="rootthread"/>
  <use name="tbb"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

# ROOT histpainter
        fname = 'roothistpainter.xml'
        contents = str("""<tool name="roothistpainter" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  <lib name="HistPainter"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
  <use name="rootimt"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

#Root X11
        fname = 'rootx11.xml'
        values['x11lib'] = '<lib name="GCocoa"/>' if sys.platform == 'darwin' else '<lib name="GX11"/>'
        contents = str("""<tool name="rootx11" version="$VER">
  <info url="http://root.cern.ch/root/"/>
  ${x11lib}
  <use name="rootcling"/>
</tool>""")
        write_scram_toolfile(contents, values, fname, prefix)

