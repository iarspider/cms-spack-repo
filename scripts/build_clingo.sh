#!/bin/bash -x

. share/spack/setup-env.sh
mkdir -p ${WORKSPACE}/opt/boostrap
spack bootstrap untrust github-actions-v0.2
spack bootstrap untrust github-actions-v0.1
spack -d solve zlib
spack -b install patchelf target=x86_64
echo build_clingo done
