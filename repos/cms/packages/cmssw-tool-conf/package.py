import os
import shutil
from collections import defaultdict

from spack import *


def local_file(fn):
    return join_path(os.path.dirname(__file__), fn)


def local_file_url(fn):
    return "file://" + local_file(fn)


class CmsswToolConf(ScramToolfilePackage, CudaPackage):
    version("52.0")

    # these go into environment
    ## INSTALL_DEPENDENCIES cmsLHEtoEOSManager gcc-fixincludes cmssw-osenv cms-git-tools
    ## UPLOAD_DEPENDENCIES dqmgui
    depends_on("scram", type="build")

    depends_on("crab")
    depends_on("cmssw-wm-tools")
    depends_on("benchmark")
    depends_on("catch2")
    depends_on("starlight")
    depends_on("alpgen")
    depends_on("boost")
    depends_on("bzip2")
    # depends_on('charybdis')
    depends_on("classlib")
    depends_on("clhep")
    depends_on("coral")
    depends_on("cppunit")
    depends_on("cpu-features")
    depends_on("curl")
    depends_on("das-client")
    depends_on("berkeley-db")
    depends_on("davix")
    depends_on("evtgen")
    depends_on("expat")
    # depends_on('fakesystem')
    depends_on("flatbuffers")
    depends_on("fmt")
    depends_on("gbl")
    # depends_on('gcc')
    depends_on("gdbm")
    depends_on("geant4")
    depends_on("cms-geant4data")
    depends_on("glimpse")
    depends_on("gmake")
    depends_on("gsl")
    depends_on("highfive")
    depends_on("hector")
    depends_on("hepmc")
    depends_on("hepmc3")
    depends_on("heppdt")
    # depends_on('herwig6')
    depends_on("herwig3")
    depends_on("hydjet")
    depends_on("hydjet2")
    depends_on("ittnotify")
    depends_on("jemalloc")
    depends_on("jemalloc-debug")  # TODO
    depends_on("jemalloc-prof")  # TODO
    # depends_on('jimmy')
    depends_on("nlohmann-json")
    depends_on("ktjet")
    depends_on("lhapdf")
    depends_on("libjpeg-turbo")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("libungif")
    depends_on("libxml2")
    depends_on("lwtnn")
    depends_on("meschach")
    depends_on("pcre2")
    # depends_on('photos-f')
    depends_on("photos")
    depends_on("pyquen")
    depends_on("pythia6")
    depends_on("pythia8")
    depends_on("python@3:")
    depends_on("root")
    depends_on("sherpa")
    depends_on("libpciaccess")
    depends_on("numactl")
    depends_on("hwloc")
    depends_on("gdrcopy")
    depends_on("rdma-core")
    depends_on("ucx")
    depends_on("openmpi")
    depends_on("sigcpp")
    depends_on("sqlite")
    # depends_on('tauola-f')
    depends_on("tauola")
    depends_on("thepeg")
    # depends_on('toprex')
    depends_on("util-linux-uuid")
    depends_on("xerces-c")
    depends_on("dcap")
    depends_on("frontier-client")
    depends_on("xrootd")
    depends_on("dd4hep")
    depends_on("valgrind")
    depends_on("cmsswdata")
    depends_on("zstd")
    depends_on("hls")
    depends_on("opencv")
    depends_on("grpc")
    depends_on("py-onnx-runtime")
    depends_on("triton-inference-client")
    depends_on("hdf5")
    # depends_on('cascade')
    depends_on("yoda")
    depends_on("fftw")
    depends_on("fftjet")
    depends_on("professor")
    depends_on("xz")
    depends_on("lz4")
    depends_on("protobuf")
    depends_on("lcov")
    depends_on("llvm")
    depends_on("tbb")
    depends_on("mctester")
    depends_on("vdt")
    depends_on("gnuplot")
    depends_on("sloccount")
    depends_on("millepede")
    depends_on("pacparser")
    depends_on("git")
    # depends_on('yaml-cpp')
    depends_on("gmp")
    depends_on("mpfr")
    depends_on("fjcontrib")
    # depends_on('opencl') # DROP?
    # depends_on('opencl-clhpp') # DROP?
    depends_on("qd")
    depends_on("blackhat")
    depends_on("sherpa")
    depends_on("geant4-parfullcms")
    depends_on("fasthadd")
    depends_on("eigen")
    depends_on("gdb")
    depends_on("libxslt")
    depends_on("giflib")
    depends_on("freetype")
    depends_on("utm")
    depends_on("libffi")
    depends_on("csctrackfinderemulation")
    depends_on("tinyxml2")
    depends_on("md5")
    depends_on("gosam-contrib")
    depends_on("py-gosam")
    depends_on("madgraph5amc")
    depends_on("python-tools")
    depends_on("dasgoclient")
    depends_on("mxnet-predict")
    depends_on("dablooms")
    depends_on("g4hepem")

    depends_on("openldap", when="platform=linux")
    depends_on("gperftools", when="platform=linux")
    depends_on("cuda", when="platform=linux")
    depends_on("cuda-compatible-runtime", when="platform=linux")
    depends_on("alpaka", when="platform=linux")
    # depends_on('cupla ', when='platform=linux')

    # depends_on('icc', when='platform=linux target=x86_64:')
    # depends_on('icx', when='platform=linux target=x86_64:')

    depends_on("cudnn", when="platform=linux target=x86_64:")
    depends_on("cudnn", when="platform=linux target=ppc64le:")

    # depends_on('rocm', when='platform=linux target=x86_64:')

    depends_on("libunwind", when="platform=linux")

    depends_on("igprof", when="platform=linux target=x86_64:")
    depends_on("igprof", when="platform=linux target=aarch64:")
    depends_on("openloops", when="platform=linux target=x86_64:")
    depends_on("openloops", when="platform=linux target=aarch64:")

    depends_on("tkonlinesw")
    depends_on("oracle-instant-client")
    depends_on("intel-vtune", when="platform=linux target=x86_64:")
    depends_on("cmsmon-tools", when="platform=linux target=x86_64:")
    depends_on("dip", when="platform=linux target=x86_64:")

    # TODO
    # depends_on('tkonlinesw-fake', when='platform=linux target=aarch64:')
    # depends_on('tkonlinesw-fake', when='platform=linux target=ppc64le:')
    # depends_on('oracle-fake', when='platform=linux target=aarch64:')
    # depends_on('oracle-fake', when='platform=linux target=ppc64le:')

    depends_on("xtensor")
    depends_on("xtl")
    depends_on("xgboost")

    # TODO: cmssw-vectorization
    depends_on("zlib")
    depends_on("fastjet")
    depends_on("vecgeom")
    depends_on("py-tensorflow")
    depends_on("openblas")
    depends_on("rivet")

    ## INCLUDE cmssw-drop-tools
    skipreqtools = (
        "jcompiler",
        "icc-cxxcompiler",
        "icc-ccompiler",
        "icc-f77compiler",
        "rivet2",
        "opencl",
        "opencl-cpp",
        "nvidia-drivers",
        "intel-vtune",
        "jemalloc-debug",
    )

    def setup_build_environment(self, env):
        super().setup_build_environment(env)
        # ScramToolfilePackage.setup_build_environment(self, env)
        if self.spec["geant4"].satisfies("+vecgeom"):
            env.set("GEANT4_HAS_VECGEOM", "YES")
        else:
            env.unset("GEANT4_HAS_VECGEOM")
