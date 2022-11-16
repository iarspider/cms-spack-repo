#!/bin/bash
if [ -z ${SPACK_VERSION+x} ]; then
  export SPACK_VERSION=v0.18.1
  echo "INFO: using default spack version ${SPACK_VERSION}"
fi

if [ -z ${SPACK_ENV_NAME+x} ]; then
  echo "SPACK_ENV_NAME not set"
  exit 1
fi

if [ -z ${SCRAM_ARCH+x} ]; then
  echo "SCRAM_ARCH not set"
  exit 1
fi

if [ -z ${WORKSPACE+x} ]; then
  echo "WORKSPACE not set"
  exit 1
fi
###############################################################################
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )/cms-spack-repo"
cd ${WORKSPACE}
# For boto3
export PYTHONPATH=/cvmfs/cms-ib.cern.ch/share/python3/lib/python3.6/site-packages:$PYTHONPATH
export S3_ENDPOINT_URL=https://s3.cern.ch
export RPM_INSTALL_PREFIX=${WORKSPACE}/install

mkdir -p $WORKSPACE/spack-tmp
export TMPDIR=$WORKSPACE/spack-tmp

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
find ${WORKSPACE}/cms-spack-repo/repos/backports/packages -maxdepth 1 -type 'd' -exec cp -r -f {} ${WORKSPACE}/spack/var/spack/repos/builtin/packages \;
echo Copying backported PythonPackage class
cp ${WORKSPACE}/cms-spack-repo/build_systems/python.py lib/spack/spack/build_systems/
cp ${WORKSPACE}/cms-spack-repo/develop/build_environment.py lib/spack/spack/build_environment.py
echo Copying patched CudaPackage class
cp ${WORKSPACE}/cms-spack-repo/build_systems/cuda.py lib/spack/spack/build_systems/
echo Patching spack
find ${WORKSPACE}/cms-spack-repo/patches/ -type 'f' -exec patch -s -p1 -i {} \;
echo Adding CMS repository
bin/spack repo add --scope=site ${WORKSPACE}/cms-spack-repo/repos/cms
echo Adding CMS mirror
bin/spack mirror add --scope=site cms s3://cms-spack/SOURCES
echo Adding CMS buildcache
bin/spack mirror add --scope=site cms-s3 s3://cms-spack/${SCRAM_ARCH}/${SPACK_ENV_NAME}
echo Adding CMS Spack signing key to trusted list
# bin/spack buildcache keys --install --trust
# Temporary workaround until `spack gpg publish` works!
wget https://test-cms-spack.web.cern.ch/test-cms-spack/CMS/mirror/build_cache/_pgp/A9541E16BC04DEA9624B99B43E5E5DB6F48CB63F.pub -O ${WORKSPACE}/cms-spack.pub
bin/spack gpg trust ${WORKSPACE}/cms-spack.pub
(bin/spack gpg list --trusted | grep -e "4096R/F48CB63F") || exit 1
if [ ! -z ${SPACK_DEVELOP} ]; then
  echo Adding spack augment command
  bin/spack config --scope=site add "config:extensions:${WORKSPACE}/cms-spack-repo/spack-scripting"
else
  echo Add padding to install_tree
  bin/spack config --scope=site add "config:install_tree:padded_length:128"
fi
echo Increasing download timeout from 10s to 5m
bin/spack config --scope=site add "config:connect_timeout:300"

echo Set install directory
bin/spack config add "config:install_tree:root:${RPM_INSTALL_PREFIX}"

if [ ! -z ${1+x} ]; then
  echo Setting CMSSW version to $1
  sed -i -e "s/#!# //" ${WORKSPACE}/cms-spack-repo/repos/cms/packages/cmssw/package.py
  sed -i -e "s/#VERSION#/$1/g" ${WORKSPACE}/cms-spack-repo/repos/cms/packages/cmssw/package.py
fi

echo Creating environment ${SPACK_ENV_NAME}
bin/spack env create ${SPACK_ENV_NAME} ${WORKSPACE}/cms-spack-repo/environments/${SPACK_ENV_NAME}/spack.yaml
echo Done
