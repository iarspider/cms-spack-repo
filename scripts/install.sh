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
bin/spack config add "config:install_tree:root:/cvmfs/cms-ib.cern.ch/spack"
mkdir -p /cvmfs/cms-ib.cern.ch/spack
echo Start the installation
cvmfs_server transaction cms-ib.cern.ch
#spack env activate ${SPACK_ENV_NAME}
# CMS post-install
if [ -z ${RPM_INSTALL_PREFIX+x} ]; then export RPM_INSTALL_PREFIX=/cvmfs/cms-ib.cern.ch/spack; fi
bin/spack -e ${SPACK_ENV_NAME} install -j$CORES --fail-fast --cache-only
if [$? -eq 0 ]; then echo Installation complete; cvmfs_server publish cms-ib.cern.ch; else echo "ERROR: Installation failed"; cvmfs_server abort cms-ib.cern.ch; fi

