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
spack env activate CMSSW_12_0_X
spack install -j$CORES --fail-fast --cache-only
spack load root
# Tests
root --version
spack unload root
spack load coral
python -c "import LCG"
