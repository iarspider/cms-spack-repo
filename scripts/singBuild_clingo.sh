#!/bin/bash -xe
[ -z ${WORKSPACE+x} ] && (echo 'ERROR: WORKSPACE not set, quitting'; exit 1)
[ -z ${RPM_INSTALL_PREFIX+x} ] && (echo 'ERROR: RPM_INSTALL_PREFIX not set, quitting'; exit 2)
[ -z ${SPACK_ENV_NAME+x} ] && (echo 'ERROR: SPACK_ENV_NAME not set, quitting'; exit 3)
[ -z ${SCRAM_ARCH+x} ] && (echo 'ERROR: SCRAM_ARCH not set, quitting'; exit 4)

export USE_SINGULARITY=true
export WORKDIR=${WORKSPACE}
if [ x$DOCKER_IMG == "x" ]; then
    arch="$(echo $SCRAM_ARCH | cut -d_ -f2)"
    os=$(echo $SCRAM_ARCH | cut -d_ -f1 | sed 's|slc7|cc7|')
    if [ "${os}" = "rhel8" ] ; then os="ubi8" ; fi
    DOCKER_IMG="cmssw/${os}:${arch}-bootstrap"
    if [ "${arch}" = "amd64" ] ; then
      DOCKER_IMG="cmssw/${os}:x86_64-bootstrap"
    fi
fi
export DOCKER_IMG

cp ${WORKSPACE}/cms-spack-repo/bootstrap/packages-$(cmsos).yaml ${WORKSPACE}/bootstrap/config/packages.yaml

${WORKSPACE}/cms-bot/docker_launcher.sh ${WORKSPACE}/cms-spack-repo/scripts/build_clingo.sh
echo I AM DONE FOR NOW, ADD COMMANDS TO UPLOAD BUILDCACHE
exit 0
