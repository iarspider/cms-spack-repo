from spack import *
from collections import defaultdict
import os
import shutil

def local_file(fn):
    return join_path(os.path.dirname(__file__), fn)

def local_file_url(fn):
    return 'file://' + local_file(fn)


class CmsswToolConf(BundlePackage, CudaPackage):
    version('52.0')
    
    resource(name='toolfiles',
             git='https://github.com/cms-sw/cmsdist.git',
             branch='CMSSW_12_4_X',
             dest='toolfiles')

    # these go into environment
    ## INSTALL_DEPENDENCIES cmsLHEtoEOSManager gcc-fixincludes cmssw-osenv cms-git-tools
    ## UPLOAD_DEPENDENCIES dqmgui
    depends_on('scram', type='build')

    depends_on('crab')
    depends_on('cmssw-wm-tools')
    depends_on('benchmark')
    depends_on('catch2')
    depends_on('starlight')
    depends_on('alpgen')
    depends_on('boost')
    depends_on('bzip2')
    depends_on('charybdis')
    depends_on('classlib')
    depends_on('clhep')
    depends_on('coral')
    depends_on('cppunit')
    depends_on('curl')
    depends_on('das_client')
    depends_on('berkeley-db')
    depends_on('davix')
    depends_on('evtgen')
    depends_on('expat')
    # depends_on('fakesystem')
    depends_on('flatbuffers')
    depends_on('fmt')
    depends_on('gbl')
    # depends_on('gcc')
    depends_on('gdbm')
    depends_on('geant4')
    depends_on('geant4data')
    depends_on('glimpse')
    depends_on('gmake')
    depends_on('gsl')
    depends_on('highfive')
    depends_on('hector')
    depends_on('hepmc')
    depends_on('hepmc3')
    depends_on('heppdt')
    depends_on('herwig')
    depends_on('herwig7')
    depends_on('hydjet')
    depends_on('hydjet2')
    depends_on('ittnotify')
    depends_on('jemalloc')
    depends_on('jemalloc-debug')
    depends_on('jimmy')
    depends_on('nlohmann-json')
    depends_on('ktjet')
    depends_on('lhapdf')
    depends_on('libjpeg-turbo')
    depends_on('libpng')
    depends_on('libtiff')
    depends_on('libungif')
    depends_on('libxml2')
    depends_on('lwtnn')
    depends_on('meschach')
    depends_on('pcre2')
    depends_on('photos-f')
    depends_on('photospp')
    depends_on('pyquen')
    depends_on('pythia6')
    depends_on('pythia8')
    depends_on('python@3:')
    depends_on('root')
    depends_on('sherpa')
    depends_on('libpciaccess')
    depends_on('numactl')
    depends_on('hwloc')
    depends_on('gdrcopy')
    depends_on('rdma-core')
    depends_on('ucx')
    depends_on('openmpi')
    depends_on('sigcpp')
    depends_on('sqlite')
    depends_on('tauola-f')
    depends_on('tauolapp')
    depends_on('thepeg')
    depends_on('toprex')
    depends_on('libuuid')
    depends_on('xerces-c')
    depends_on('dcap')
    depends_on('frontier_client')
    depends_on('xrootd')
    depends_on('dd4hep')
    depends_on('valgrind')
    depends_on('cmsswdata')
    depends_on('zstd')
    depends_on('hls')
    depends_on('opencv')
    depends_on('grpc')
    depends_on('onnxruntime')
    depends_on('triton-inference-client')
    depends_on('hdf5')
    depends_on('cascade')
    depends_on('yoda')
    depends_on('fftw3')
    depends_on('fftjet')
    depends_on('professor2')
    depends_on('xz')
    depends_on('lz4')
    depends_on('protobuf')
    depends_on('lcov')
    depends_on('llvm')
    depends_on('tbb')
    depends_on('mctester')
    depends_on('vdt')
    depends_on('icc')
    depends_on('gnuplot')
    depends_on('sloccount')
    depends_on('millepede')
    depends_on('pacparser')
    depends_on('git')
    depends_on('yaml-cpp')
    depends_on('gmp-static')
    depends_on('mpfr-static')
    depends_on('fastjet-contrib')
    depends_on('opencl')
    depends_on('opencl-cpp')
    depends_on('qd')
    depends_on('blackhat')
    depends_on('sherpa')
    depends_on('geant4-parfullcms')
    depends_on('fasthadd')
    depends_on('eigen')
    depends_on('gdb')
    depends_on('libxslt')
    depends_on('giflib')
    depends_on('freetype')
    depends_on('utm')
    depends_on('libffi')
    depends_on('csctrackfinderemulation')
    depends_on('tinyxml2')
    depends_on('md5')
    depends_on('gosamcontrib')
    depends_on('gosam')
    depends_on('madgraph5amcatnlo')
    depends_on('python_tools')
    depends_on('dasgoclient')
    depends_on('mxnet-predict')
    depends_on('dablooms')

    depends_on('openldap', when='platform=linux')
    depends_on('gperftools', when='platform=linux')
    depends_on('cuda', when='platform=linux')
    depends_on('cuda-compatible-runtime', when='platform=linux')
    depends_on('alpaka', when='platform=linux')
    depends_on('cupla ', when='platform=linux')
    
    depends_on('cudnn', when='platform=linux target=x86_64:')
    depends_on('cudnn', when='platform=linux target=ppc64le:')
    
    depends_on('libunwind', when='platform=linux')

    depends_on('igprof', when='platform=linux target=x86_64:')
    depends_on('igprof', when='platform=linux target=aarch64:')
    depends_on('openloops', when='platform=linux target=x86_64:')
    depends_on('openloops', when='platform=linux target=aarch64:')
    
    depends_on('tkonlinesw', when='platform=linux arch=x86_64:')
    depends_on('oracle', when='platform=linux arch=x86_64:')
    depends_on('intel-vtune', when='platform=linux arch=x86_64:')
    depends_on('cmsmon-tools', when='platform=linux arch=x86_64:')
    depends_on('dip', when='platform=linux arch=x86_64:')

    depends_on('tkonlinesw-fake', when='platform=linux arch=aarch64:')
    depends_on('tkonlinesw-fake', when='platform=linux arch=ppc64le:')
    depends_on('oracle-fake', when='platform=linux arch=aarch64:')
    depends_on('oracle-fake', when='platform=linux arch=ppc64le:')

    depends_on('xtensor')
    depends_on('xtl')
    depends_on('xgboost')

    # TODO: cmssw-vectorization
    
    ## INCLUDE cmssw-drop-tools
    skipreqtools = ('jcompiler', 'icc-cxxcompiler', 'icc-ccompiler', 'icc-f77compiler', 'rivet2', 'opencl', 'opencl-cpp', 'nvidia-drivers', 'intel-vtune', 'jemalloc-debug')

    ## INCLUDE scram-tools.file/tool-env
    def setup_build_environment(self, env):
        env.set('ROOT_CXXMODULES', 0)
        # TODO: vectorization
        # compilation_flags.file
        if self.spec.satisfies('arch=x86_64:'):
            env.set('COMPILER_CXXFLAGS', '-msse3')
        elif self.spec.satisfies('arch=aarch64:'):
            env.set('COMPILER_CXXFLAGS', '-march=armv8-a -mno-outline-atomics')
        elif self.spec.satisfies('arch=ppc64le:'):
            env.set('COMPILER_CXXFLAGS', '-mcpu=power8 -mtune=power8 --param=l1-cache-size=64 --param=l1-cache-line-size=128 --param=l2-cache-size=512')

        env.set('ORACLE_ENV_ROOT', '')
        
        # TODO: remember, the list is different for arm vs. everything else
        env.set('CUDA_FLAGS', CudaPackage.cuda_flags(self.spec.variant['cuda_arch']))
        env.set('CUDA_HOST_CXXFLAGS', '-std=c++17')
        
        # Technical variables
        env.set('SCRAMV1_ROOT', self.spec['scram'].prefix)
        
        python_dir = 'python{0}'.format(self.spec['python'].version.up_to(2))
        env.set('PYTHON3_LIB_SITE_PACKAGES', os.path.join('lib', python_dir, 'site-packages'))
        
    ## INCLUDE scram-tool-conf
    def install(self, spec, prefix):
        mkdirp(prefix.tools.selected)
        mkdirp(prefix.tools.available)

        bash = which('bash')

        for dep in spec.dependencies():
            uctool = dep.name.upper().replace('-', '_')
            toolbase = dep.prefix
            toolver = str(dep.version)
            bash('scram-tools/bin/get_tools', toolbase, toolver, prefix, dep.name)
            
        bash('scram-tools/bin/get_tools', "", "system", prefix, "systemtools")
        
        # TODO: vectorization
        for tool in skipreqtools:
            if os.path.exists(join_path(prefix, 'tools', 'selected', tool + '.xml')):
                shutil.move(join_path(prefix, 'tools', 'selected', tool + '.xml'),
                            join_path(prefix, 'tools', 'available', tool + '.xml'))
                
        bash(join_path(os.path.dirname(__file__), '-e', 'scram-check.sh'), prefix)
        ### bash(join_path(os.path.dirname(__file__), 'generate-python-paths.sh'), prefix) ###
        ALL_PY_BIN = set()
        ALL_PY_PKGS = set()
        DUP_BIN = defaultdict(list)
        
        for pkg in spec.dependencies():
            pk_name = spec.name.lower()
            if os.path.exists(join_path(os.path.dirname(__file__), pk_name + '.xml')):
                continue
            
            pk_ver = pkg.version
            uctool = pk_name.upper().replace('-', '_')
            with open(join_path(prefix, 'tools', 'selected', pk_name + '.xml'), 'w') as f:
                f.write(f'<tool name="{pk_name}" version="{pk_ver}"\n')
                if os.path.exists(pkg.prefix.bin):
                    for b in os.listdir(pkg.prefix.bin):
                        if b in ALL_PY_BIN:
                            DUP_BIN[b].append(pk_name)
                    f.write('  <client>\n')
                    f.write(f'    <environment name="${uctool}_BASE" default="{pkg.prefix}"/>\n')
                    f.write('  </client>\n')
                    f.write(f'  <runtime name="PATH" value={uctool}/bin" type="path"/>\n')
                f.write('</tool>\n')
            
        if DUP_BIN:
            msg = '\n'.join(f'{k}: {','.join(v)}' for k, v in DUP_BIN.items())
            msg += '\nERROR: Duplicate python binaries found. Please cleanup and make sure only one binary is available.'
            raise RuntimeError(msg)
