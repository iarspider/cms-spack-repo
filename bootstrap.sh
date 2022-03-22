#!/bin/bash
SPACK_VERSION="v0.17.1"
SPACK_ENV_NAME=${SPACK_ENV_NAME:-CMSSW_12_1_X}
###############################################################################
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd ${SCRIPT_DIR}
echo This script will install Spack and configure it for CMS needs
echo Cloning spack...
[ ! -d spack ] && git clone --quiet https://github.com/spack/spack.git
cd spack; git checkout --quiet ${SPACK_VERSION}
echo Configuring spack
cp ${SCRIPT_DIR}/config/config.yaml etc/spack/
echo Adding external gcc
mkdir -p etc/spack/linux
cp ${SCRIPT_DIR}/config/compilers.yaml etc/spack/linux/compilers.yaml
echo Adding CMS hooks
cp ${SCRIPT_DIR}/hook/* lib/spack/spack/hooks/
echo Adding SCRAM build system support
cp ${SCRIPT_DIR}/build_systems/scram.py lib/spack/spack/build_systems/
echo "from spack.build_systems.scram import ScramPackage" >> lib/spack/spack/pkgkit.py
echo Adding G4data package type
cp ${SCRIPT_DIR}/build_systems/g4data.py lib/spack/spack/build_systems/
echo "from spack.build_systems.g4data import G4DataPackage" >> lib/spack/spack/pkgkit.py
echo Adding Crab package type
cp ${SCRIPT_DIR}/build_systems/crab.py lib/spack/spack/build_systems/
echo "from spack.build_systems.crab import CrabPackage" >> lib/spack/spack/pkgkit.py
echo Adding CMSData package type
cp ${SCRIPT_DIR}/build_systems/cmsdata.py lib/spack/spack/build_systems/
echo "from spack.build_systems.cmsdata import CMSDataPackage" >> lib/spack/spack/pkgkit.py
echo Copying backported recipes
##spack repo add --scope=site ${SCRIPT_DIR}/repos/backport
find ${SCRIPT_DIR}/repos/backport/packages -maxdepth 1 -type 'd' -exec cp -r -f {} ${SCRIPT_DIR}/spack/var/spack/repos/builtin/packages \;
echo Copying backported PythonPackage class
cp ${SCRIPT_DIR}/build_systems/python.py lib/spack/spack/build_systems/
cp ${SCRIPT_DIR}/develop/build_environment.py lib/spack/spack/build_environment.py
echo Initializing Spack
#source share/spack/setup-env.sh
echo Adding CMS repository
bin/spack repo add --scope=site ${SCRIPT_DIR}/repos/cms
echo Adding CMS mirror
bin/spack mirror add --scope=site cms https://test-cms-spack.web.cern.ch/test-cms-spack/CMS/mirror
echo Creating environment
bin/spack env create ${SPACK_ENV_NAME} ${SCRIPT_DIR}/environments/${SPACK_ENV_NAME}/spack.yaml
echo Done
