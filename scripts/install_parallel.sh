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
spack config add "modules:default:roots:tcl::${RPM_INSTALL_PREFIX}/modules"
spack config add "modules:default:tcl:all:autoload::all"
# spack config add "modules:default:tcl:hash_length::0"
wget -O ${WORKSPACE}/spack/var/spack/environments/${SPACK_ENV_NAME}/spack.lock https://test-razumov.web.cern.ch/test-razumov/CMS/environment/spack-${SPACK_ENV_NAME}-${SCRAM_ARCH}.lock
if [ $? -ne 0 ]; then
    echo "ERROR: couldn't fetch spack.lock"
    exit 1
fi

# Check for possible prefix conflicts
# TODO
#${WORKSPACE}/cms-spack-repo/scripts/clean-db.py
#if [ $? -ne 0 ]; then
#    echo "ERROR: db cleanup failed"
#    exit 1
#fi

#spack ${SPACK_DEBUG_FLAG} install -j"$CORES" --fail-fast --reuse --cache-only
spack ${SPACK_DEBUG_FLAG} env depfile -o Makefile --use-buildcache only
make -j"${CORES}"
exit_code=$?
if [ ${exit_code} -eq 0 ]; then
    echo Installation complete
else
    echo "ERROR: Installation failed"
    touch $WORKSPACE/fail
    exit ${exit_code}
fi

echo Regenerating tcl modules
spack ${SPACK_DEBUG_FLAG} module tcl refresh -y --delete-tree

echo Executing postinstall scripts
${WORKSPACE}/cms-spack-repo/scripts/runpost.sh
echo All done
