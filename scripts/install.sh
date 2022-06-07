#!/bin/bash

# if [ -z ${RPM_INSTALL_PREFIX+x} ]; then export RPM_INSTALL_PREFIX=/cvmfs/cms-ib.cern.ch/spack; fi
if [[ "${RPM_INSTALL_PREFIX}" != /* ]]; then RPM_INSTALL_PREFIX=${WORKSPACE}/${RPM_INSTALL_PREFIX}; fi

if [ "$(uname)" == "Darwin" ]; then
	CORES=$(sysctl -n hw.ncpu)
elif [ "$(uname)" == "Linux" ]; then
	CORES=$(awk '/^processor/ { N++} END { print N }' /proc/cpuinfo)
fi
export CORES
echo Setup Spack for CMS
cd "$WORKSPACE"/cms-spack-repo
bash -xe ./bootstrap.sh || (echo "Boostrap failed"; exit 1)
cd spack
export SPACK_DISABLE_LOCAL_CONFIG=true
export SPACK_USER_CACHE_PATH=$WORKSPACE
# source share/spack/setup-env.sh
echo Add signing key
bin/spack buildcache keys --force --install --trust
echo Set install root
bin/spack config add "config:install_tree:root:${RPM_INSTALL_PREFIX}"
echo Start the installation
if [[ "${RPM_INSTALL_PREFIX}" == /cvmfs* ]]; then cvmfs_server transaction cms-ib.cern.ch; fi
mkdir -p "${RPM_INSTALL_PREFIX}"
#spack env activate ${SPACK_ENV_NAME}
bin/spack -e "${SPACK_ENV_NAME}" install -j"$CORES" --fail-fast --cache-only --require-full-hash-match
if [$? -eq 0 ]; then
    echo Installation complete
    if [[ "${RPM_INSTALL_PREFIX}" == /cvmfs* ]]; then cvmfs_server publish cms-ib.cern.ch; fi
else
    echo "ERROR: Installation failed";
    if [[ "${RPM_INSTALL_PREFIX}" == /cvmfs* ]]; then cvmfs_server abort cms-ib.cern.ch; fi
fi
# Simple test
bin/spack -e "${SPACK_ENV_NAME}" find -p cmssw
