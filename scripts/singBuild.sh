#!/bin/bash -xe
[ -z ${WORKSPACE+x} ] && (echo 'ERROR: WORKSPACE not set, quitting'; exit 1)
[ -z ${RPM_INSTALL_PREFIX+x} ] && (echo 'ERROR: RPM_INSTALL_PREFIX not set, quitting'; exit 2)

export SPACK_ENV_NAME=${SPACK_ENV_NAME:=$RELEASE_QUEUE}
if [ -z ${SPACK_ENV_NAME+x} ]; then
  echo 'ERROR: SPACK_ENV_NAME or/and RELEASE_QUEUE not set, quitting'
  exit 1
fi

export SCRAM_ARCH=${SCRAM_ARCH:=$ARCHITECTURE}
if [ -z ${SCRAM_ARCH+x} ]; then
  echo 'ERROR: SCRAM_ARCH or/and ARCHITECTURE not set, quitting'
  exit 1
fi

export USE_SINGULARITY=true
export WORKDIR=${WORKSPACE}
if [ x$DOCKER_IMG == "x" ]; then
    arch="$(echo $SCRAM_ARCH | cut -d_ -f2)"
    os=$(echo $SCRAM_ARCH | cut -d_ -f1 | sed 's|slc7|cc7|')
    if [ "${os}" = "rhel8" ] ; then os="ubi8" ; fi
    DOCKER_IMG="cmssw/${os}:${arch}"
    if [ "${arch}" = "amd64" ] ; then
      DOCKER_IMG="cmssw/${os}:x86_64"
    fi
fi
export DOCKER_IMG

rm -f ${WORKSPACE}/fail

if [ ! -e ${WORKSPACE}/spack ]; then
  bash -xe ${WORKSPACE}/cms-spack-repo/bootstrap.sh $1 || (echo Bootstrap failed; exit 1)
fi

#if [ ! -z ${1+x} ]; then
#  echo Setting CMSSW version to $1
#  VERSION=$(echo $1 | sed -e 's#/#_#g'
#  sed -i -e "s/#!# //" ${WORKSPACE}/cms-spack-repo/repos/cms/packages/cmssw/package.py
#  sed -i -e "s/#VERSION#/$VERSION/g" ${WORKSPACE}/cms-spack-repo/repos/cms/packages/cmssw/package.py
#  sed -i -e "s/#TAG#/$1/g" ${WORKSPACE}/cms-spack-repo/repos/cms/packages/cmssw/package.py
#fi

${WORKSPACE}/cms-bot/docker_launcher.sh ${WORKSPACE}/cms-spack-repo/scripts/build.sh
if [ -e ${WORKSPACE}/fail ]; then
    touch ${WORKSPACE}/fail
    exit 1
fi
echo All done
