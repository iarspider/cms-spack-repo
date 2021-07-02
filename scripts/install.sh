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
# echo Add signing key
# spack gpg trust $SPACK_GPG_KEY
echo Start the installation
spack env activate CMSSW_12_0_X
spack install -j$CORES --fail-fast --cache-only
spack load coral
# Tests
root --version
python -c "import LCG"
