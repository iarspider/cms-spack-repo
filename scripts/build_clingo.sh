#!/bin/bash -x

cp ${WORKSPACE}/cms-spack-repo/bootstrap/packages-$(cmsos).yaml ${WORKSPACE}/bootstrap/config/packages.yaml

pushd ${WORKSPACE}/spack
. share/spack/setup-env.sh
spack bootstrap untrust github-actions-v0.2
spack bootstrap untrust github-actions-v0.1
spack -d solve zlib
spack -b install patchelf target=x86_64
spack bootstrap trust github-actions-v0.2
popd
echo build_clingo done
