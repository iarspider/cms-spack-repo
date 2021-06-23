#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd ${SCRIPT_DIR}
SPACK_VERSION="729d66a3f8"
echo This script will install Spack and configure it for CMS needs
echo Cloning spack...
git clone https://github.com/spack/spack.git -b ${SPACK_VERSION}
echo Initializing Spack
cd spack
source spack/share/setup-env.sh
echo Adding CMS repository
spack repo add --scope=site ${SCRIPT_DIR}
echo Configuring spack
cp ${SCRIPT_DIR}/config/config.yaml etc/spack/
echo Adding external gcc 9.3.0
mkdir -p etc/spack/linux
cp ${SCRIPT_DIR}/config/compilers.yaml etc/spack/linux/compilers.yaml
echo Adding CMS hooks
cp ${SCRIPT_DIR}/hook/* lib/spack/spack/hooks/
echo Adding SCRAM build system support
cp ${SCRIPT_DIR}/scram.py lib/spack/spack/build_systems/
echo Creating environment
spack env create CMSSW_12_0_X ${SCRIPT_DIR}/environments/CMSSW_12_0_X/spack.yaml
echo Done