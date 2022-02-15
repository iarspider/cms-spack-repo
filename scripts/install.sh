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
source share/spack/setup-env.sh 
echo Add signing key
spack buildcache keys --force --install --trust 
echo Set install root
mkdir -p $WORKSPACE/install
spack config add "config:install_tree:root:$WORKSPACE/install"
echo Start the installation
spack env activate CMSSW_12_1_X
spack install -j$CORES --fail-fast --cache-only
# CMS post-install
if [ -z ${RPM_INSTALL_PREFIX+x} ]; then export RPM_INSTALL_PREFIX=$WORKSPACE; fi
find $WORKSPACE/install -name 'cmspost.sh' -exec /bin/bash -xe {} \;
# Tests
spack load root
root --version
spack unload root
spack load coral
python -c "import LCG"
spack unload coral