#!/bin/bash
SPACK_VERSION=${SPACK_VERSION:-v0.17.1}
SPACK_ENV_NAME=${SPACK_ENV_NAME:-CMSSW_12_1_X}
###############################################################################
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/cms-spack-repo"
cd ${WORKSPACE}
# For boto3
export PYTHONPATH=/cvmfs/cms-ib.cern.ch/share/python3/lib/python3.6/site-packages:$PYTHONPATH
export S3_ENDPOINT_URL=https://s3.cern.ch
export RPM_INSTALL_PREFIX=${WORKSPACE}/install

echo This script will install Spack and configure it for CMS needs
if [ -d ${WORKSPACE}/spack ] ; then
  echo Skipping bootstrap
  exit 0
fi

echo Cloning spack from branch ${SPACK_VERSION}...
git clone --quiet https://github.com/spack/spack.git ${WORKSPACE}/spack
cd ${WORKSPACE}/spack; git checkout --quiet ${SPACK_VERSION}
echo Configuring spack
cp ${WORKSPACE}/cms-spack-repo/config/config.yaml etc/spack/
echo Adding external gcc
mkdir -p etc/spack/linux
cp ${WORKSPACE}/cms-spack-repo/config/compilers.yaml etc/spack/linux/compilers.yaml
echo Forcing use of external gcc for bootstrapping
mkdir -p ${WORKSPACE}/bootstrap/config/linux
cp ${WORKSPACE}/cms-spack-repo/config/compilers.yaml ${WORKSPACE}/bootstrap/config/linux/
if [[ "${SCRAM_ARCH}" = *"amd64"* ]]; then
   sed -i -e 's/core2/x86_64/g' ${WORKSPACE}/bootstrap/config/linux/compilers.yaml
fi
echo Adding CMS hooks
cp ${WORKSPACE}/cms-spack-repo/hook/* lib/spack/spack/hooks/
echo Adding SCRAM build system support
cp ${WORKSPACE}/cms-spack-repo/build_systems/scram.py lib/spack/spack/build_systems/
echo "from spack.build_systems.scram import ScramPackage" >> lib/spack/spack/pkgkit.py
echo Adding SCRAM toolfile package class
cp ${WORKSPACE}/cms-spack-repo/build_systems/scramtoolfile.py lib/spack/spack/build_systems/
echo "from spack.build_systems.scramtoolfile import ScramToolfilePackage" >> lib/spack/spack/pkgkit.py
echo Adding Crab package type
cp ${WORKSPACE}/cms-spack-repo/build_systems/crab.py lib/spack/spack/build_systems/
echo "from spack.build_systems.crab import CrabPackage" >> lib/spack/spack/pkgkit.py
echo Adding CMSData package type
cp ${WORKSPACE}/cms-spack-repo/build_systems/cmsdata.py lib/spack/spack/build_systems/
echo "from spack.build_systems.cmsdata import CMSDataPackage" >> lib/spack/spack/pkgkit.py
echo Copying backported recipes
find ${WORKSPACE}/cms-spack-repo/repos/backport/packages -maxdepth 1 -type 'd' -exec cp -r -f {} ${WORKSPACE}/spack/var/spack/repos/builtin/packages \;
echo Copying backported PythonPackage class
cp ${WORKSPACE}/cms-spack-repo/build_systems/python.py lib/spack/spack/build_systems/
cp ${WORKSPACE}/cms-spack-repo/develop/build_environment.py lib/spack/spack/build_environment.py
echo Copying patched CudaPackage class
cp ${WORKSPACE}/cms-spack-repo/build_systems/cuda.py lib/spack/spack/build_systems/
echo Patching spack.util.web and spack.s3_handler
patch -s -p1 < ${WORKSPACE}/cms-spack-repo/s3.patch
echo Patching spack.buildcache to only relocate things that needs to be relocated
patch -s -p1 < ${WORKSPACE}/cms-spack-repo/31074_buildcache.patch
echo Adding CMS repository
bin/spack repo add --scope=site ${WORKSPACE}/cms-spack-repo/repos/cms
echo Adding CMS mirror
bin/spack mirror add --scope=site cms https://test-cms-spack.webtest.cern.ch/test-cms-spack/CMS/mirror/
echo Adding CMS buildcache
bin/spack mirror add --scope=site cms-s3 s3://cms-spack
echo Adding CMS Spack signing key to trusted list
#bin/spack buildcache keys --install --trust
# Temporary workaround until `spack gpg publish` works!
wget https://test-cms-spack.web.cern.ch/test-cms-spack/CMS/mirror/build_cache/_pgp/A9541E16BC04DEA9624B99B43E5E5DB6F48CB63F.pub -O ${WORKSPACE}/cms-spack.pub
bin/spack gpg trust ${WORKSPACE}/cms-spack.pub
(bin/spack gpg list --trusted | grep -e "4096R/F48CB63F") || exit 1
if [ ! -z ${SPACK_DEVELOP} ]; then
  echo Adding spack augment command
  bin/spack config --scope=site add "config:extensions:${WORKSPACE}/cms-spack-repo/spack-scripting"
else
  echo Add padding to install_tree
  bin/spack config add "config:install_tree:padded_length:128"
fi
echo Set install directory
bin/spack config add "config:install_tree:root:${RPM_INSTALL_PREFIX}"
echo Creating environment ${SPACK_ENV_NAME}
sed -i -e "s#@SCRAM_ARCH@#${SCRAM_ARCH}#g" ${WORKSPACE}/cms-spack-repo/environments/${SPACK_ENV_NAME}/spack.yaml
bin/spack env create ${SPACK_ENV_NAME} ${WORKSPACE}/cms-spack-repo/environments/${SPACK_ENV_NAME}/spack.yaml
echo Done
