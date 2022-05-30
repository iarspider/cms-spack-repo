#!/bin/bash
if [ `uname` == "Darwin" ]; then
	CORES=`sysctl -n hw.ncpu`
elif [ `uname` == "Linux" ]; then
	CORES=`awk '/^processor/ { N++} END { print N }' /proc/cpuinfo`
fi
export CORES
echo Setup Spack for CMS
cd $WORKSPACE/cms-spack-repo
bash -xe ./bootstrap.sh
cd spack
export SPACK_DISABLE_LOCAL_CONFIG=true
export SPACK_USER_CACHE_PATH=$WORKSPACE
# source share/spack/setup-env.sh
echo Add signing key
bin/spack buildcache keys --force --install --trust
echo Set install root
mkdir -p $WORKSPACE/install
bin/spack config add "config:install_tree:root:$WORKSPACE/install"
echo Start the installation
#spack env activate ${SPACK_ENV_NAME}
# CMS post-install
if [ -z ${RPM_INSTALL_PREFIX+x} ]; then export RPM_INSTALL_PREFIX=$WORKSPACE/root; fi
bin/spack -e ${SPACK_ENV_NAME} install -j$CORES --fail-fast --cache-only
# Tests
if [[ ${SPACK_ENV_NAME} == CMSSW* ]]; then
    source share/spack/setup-env.sh
    spack env activate ${SPACK_ENV_NAME}
    spack find -p root | grep cvmfs
#    spack load root
#    root --version
#    spack unload
#    spack load coral
#    python -c "import LCG"
#    spack unload coral
fi
