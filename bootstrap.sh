#!/bin/bash
SPACK_VERSION=${SPACK_VERSION:-v0.18.0}
SPACK_ENV_NAME=${SPACK_ENV_NAME:-CMSSW_12_4_X}
###############################################################################
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
WORKSPACE=${WORKSPACE:-$(cd $SCRIPT_DIR/..; pwd)}
cd ${WORKSPACE}
# For boto3
export PYTHONPATH=/cvmfs/cms-ib.cern.ch/share/python3/lib/python3.6/site-packages:$PYTHONPATH
export S3_ENDPOINT_URL=https://s3.cern.ch

echo This script will install Spack and configure it for CMS needs
[ -d spack ] && (echo Skipping bootstrap; exit 0)
echo Cloning spack: ${SPACK_VERSION}...
git clone --quiet https://github.com/spack/spack.git
cd ${WORKSPACE}/spack; git checkout --quiet ${SPACK_VERSION}
export SPACK_DISABLE_LOCAL_CONFIG=true
export SPACK_USER_CACHE_PATH=$WORKSPACE
cd ${WORKSPACE}/spack
. share/spack/setup-env.sh
echo Adding external gcc
mkdir -p etc/spack/linux
cp ${SCRIPT_DIR}/config/compilers.yaml etc/spack/linux/compilers.yaml
echo Adding CMS hooks
cp ${SCRIPT_DIR}/hook/* lib/spack/spack/hooks/
echo Adding SCRAM build system support
cp ${SCRIPT_DIR}/build_systems/scram.py lib/spack/spack/build_systems/
echo "from spack.build_systems.scram import ScramPackage" >> lib/spack/spack/pkgkit.py
echo Adding SCRAM toolfile package class
cp ${SCRIPT_DIR}/build_systems/scramtoolfile.py lib/spack/spack/build_systems/
echo "from spack.build_systems.scramtoolfile import ScramToolfilePackage" >> lib/spack/spack/pkgkit.py
echo Adding Crab package type
cp ${SCRIPT_DIR}/build_systems/crab.py lib/spack/spack/build_systems/
echo "from spack.build_systems.crab import CrabPackage" >> lib/spack/spack/pkgkit.py
echo Adding CMSData package type
cp ${SCRIPT_DIR}/build_systems/cmsdata.py lib/spack/spack/build_systems/
echo "from spack.build_systems.cmsdata import CMSDataPackage" >> lib/spack/spack/pkgkit.py
echo Copying backported recipes
if [ -d ${SCRIPT_DIR}/repos/backport ]; then
  find ${SCRIPT_DIR}/repos/backport/packages -maxdepth 1 -type 'd' -exec cp -r -f {} ${WORKSPACE}/spack/var/spack/repos/builtin/packages \;
fi
echo Patching spack.util.web and spack.s3_handler
patch -p1 < ${SCRIPT_DIR}/s3.patch
echo Patching buildcache create
patch -p1 < ${SCRIPT_DIR}/31074_buildcache.patch
echo Adding CMS repository
spack repo add --scope=site ${SCRIPT_DIR}/repos/cms
echo Adding CMS mirror
spack mirror add --scope=site cms https://test-cms-spack.web.cern.ch/test-cms-spack/CMS/mirror
echo Adding CMS buildcache
spack mirror add --scope=site cms-s3 s3://cms-spack
echo Adding CMS Spack signing key to trusted list
##spack buildcache keys --install --trust
# Temporary workaround until `spack gpg publish` works!
wget https://test-cms-spack.web.cern.ch/test-cms-spack/CMS/mirror/build_cache/_pgp/A9541E16BC04DEA9624B99B43E5E5DB6F48CB63F.pub -O ${WORKSPACE}/cms-spack.pub
spack gpg trust ${WORKSPACE}/cms-spack.pub
echo Adding spack augment command
spack config --scope=site add "config:extensions:${SCRIPT_DIR}/spack-scripting"
echo Get patchelf
GCC_VER=$(gcc --version | head -1 | cut -d ' ' -f 3)
spack compiler find --scope=site
# --cache-only
spack install --reuse patchelf%gcc@${GCC_VER} || exit 1
spack load patchelf%gcc@${GCC_VER}
echo Force bootstrap
spack -d solve zlib || exit 1
echo Creating environment ${SPACK_ENV_NAME}
spack env create ${SPACK_ENV_NAME} ${SCRIPT_DIR}/environments/${SPACK_ENV_NAME}/spack.yaml
echo Done
