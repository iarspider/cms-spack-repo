#!/bin/bash -x
[ -z ${WORKSPACE+x} ] && (echo 'ERROR: WORKSPACE not set, quitting'; exit 1)
[ -z ${RPM_INSTALL_PREFIX+x} ] && (echo 'ERROR: RPM_INSTALL_PREFIX not set, quitting'; exit 2)
[ -z ${SPACK_ENV_NAME+x} ] && (echo 'ERROR: SPACK_ENV_NAME not set, quitting'; exit 3)
[ -z ${CMSARCH+x} ] && (echo 'ERROR: CMSARCH not set, quitting'; exit 4)

export CMSARCH=${CMSARCH:-slc7_amd64_gcc900}
export SCRAM_ARCH=$CMSARCH
export USE_SINGULARITY=true
export WORKDIR=${WORKSPACE}
if [ x$DOCKER_IMG == "x" ]; then
    arch="$(echo $CMSARCH | cut -d_ -f2)"
    os=$(echo $CMSARCH | cut -d_ -f1 | sed 's|slc7|cc7|')
    if [ "${os}" = "rhel8" ] ; then os="ubi8" ; fi
    DOCKER_IMG="cmssw/${os}:${arch}"
    if [ "${arch}" = "amd64" ] ; then
      DOCKER_IMG="cmssw/${os}:x86_64"
    fi
fi
export DOCKER_IMG

rm -f ${WORKSPACE}/fail
rm -f ${WORKSPACE}/spack/var/spack/environments/${SPACK_ENV_NAME}/spack.lock
rm -rf ${WORKSPACE}/spack/var/spack/environments/${SPACK_ENV_NAME}/.spack-env/

bash -xe ${WORKSPACE}/cms-spack-repo/bootstrap.sh

${WORKSPACE}/cms-bot/docker_launcher.sh ${WORKSPACE}/cms-spack-repo/scripts/build.sh
if [ -e ${WORKSPACE}/fail ]; then
#    echo Build falied, uploading monitor data
#    tar -zcf ${WORKSPACE}/monitor.tar.gz ${WORKSPACE}/monitor
#    scp ${WORKSPACE}/monitor.tar.gz cmsbuild@lxplus:/eos/user/r/razumov/www/CMS/mirror
#    rm ${WORKSPACE}/monitor.tar.gz
    touch ${WORKSPACE}/fail
    exit 1
fi
if [ ${UPLOAD_BUILDCACHE-x} = "true" ]; then
  echo Prepare mirror and buildcache
  # TODO: create mirror and sync to s3
  # TODO: push gpg key to mirror (broken in 0.17, should be working in 0.18)
  bin/spack -e ${SPACK_ENV_NAME} buildcache create -r -a --mirror-url s3://cms-spack/
fi
echo All done
