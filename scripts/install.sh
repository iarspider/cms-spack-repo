#!/bin/bash -x
# For boto3
export PYTHONPATH=/cvmfs/cms-ib.cern.ch/share/python3/lib/python3.6/site-packages:$PYTHONPATH
export PYTHONUNBUFFERED=1
export S3_ENDPOINT_URL=https://s3.cern.ch

if [[ "${RPM_INSTALL_PREFIX}" != /* ]]; then RPM_INSTALL_PREFIX=${WORKSPACE}/${RPM_INSTALL_PREFIX}; fi

if [ "$(uname)" == "Darwin" ]; then
	CORES=$(sysctl -n hw.ncpu)
elif [ "$(uname)" == "Linux" ]; then
	CORES=$(awk '/^processor/ { N++} END { print N }' /proc/cpuinfo)
fi
export CORES
cd ${WORKSPACE}/spack
export SPACK_DISABLE_LOCAL_CONFIG=true
export SPACK_USER_CACHE_PATH=$WORKSPACE
source share/spack/setup-env.sh
#echo Add signing key
#spack buildcache keys --force --install --trust
echo Set install root
spack config add "config:install_tree:root:${RPM_INSTALL_PREFIX}/${SCRAM_ARCH}"

SPACK_DEBUG_FLAG=""
if [ ! -z ${SPACK_DEBUG+x} ]; then
  SPACK_DEBUG_FLAG="-d --stacktrace"
fi

echo Start the installation
mkdir -p "${RPM_INSTALL_PREFIX}"
spack env activate ${SPACK_ENV_NAME}
spack ${SPACK_DEBUG_FLAG} -e "${SPACK_ENV_NAME}" install -j"$CORES" --fail-fast --reuse --cache-only
exit_code=$?
if [ ${exit_code} -eq 0 ]; then
    echo Installation complete
else
    echo "ERROR: Installation failed"
    touch $WORKSPACE/fail
    exit ${exit_code}
fi

echo Executing postinstall scripts
${WORKSPACE}/cms-spack-repo/scripts/runpost.sh
echo All done
