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
    DOCKER_IMG="cmssw/${os}:${arch}"
    if [ "${arch}" = "amd64" ] ; then
      DOCKER_IMG="cmssw/${os}:x86_64"
    fi
fi
export DOCKER_IMG

rm -f ${WORKSPACE}/fail
#rm -f ${WORKSPACE}/spack/var/spack/environments/${SPACK_ENV_NAME}/spack.lock
#rm -rf ${WORKSPACE}/spack/var/spack/environments/${SPACK_ENV_NAME}/.spack-env/

[ ! -e ${WORKSPACE}/spack ] && bash -xe ${WORKSPACE}/cms-spack-repo/bootstrap.sh

${WORKSPACE}/cms-bot/docker_launcher.sh ${WORKSPACE}/cms-spack-repo/scripts/build.sh
if [ ${exit_code} -ne 0 ]; then
    echo Build failed, uploading logs
    ssh $SSH_OPTS lxplus rm -rf /eos/user/r/razumov/www/CMS/logs/${SPACK_ENV_NAME}-${SCRAM_ARCH}
    ssh $SSH_OPTS lxplus mkdir /eos/user/r/razumov/www/CMS/logs/${SPACK_ENV_NAME}-${SCRAM_ARCH}
    pushd ${WORKSPACE}/spack/stage
    find . -maxdepth 1 -type d -name 'spack-stage-*' -print0 | while read -d $'\0' dirn
    do
        ssh $SSH_OPTS lxplus mkdir /eos/user/r/razumov/www/CMS/logs/${SPACK_ENV_NAME}-${SCRAM_ARCH}/$dirn
        scp $SSH_OPTS $d/*.txt lxplus:/eos/user/r/razumov/www/CMS/logs/${SPACK_ENV_NAME}-${SCRAM_ARCH}/$dirn
    done
    popd
    scp $SSH_OPTS ${WORKSPACE}/spack/var/spack/environments/${SPACK_ENV_NAME}/spack.lock lxplus:/eos/user/r/razumov/www/CMS/logs/${SPACK_ENV_NAME}-${SCRAM_ARCH}/
    touch $WORKSPACE/fail
    exit ${exit_code}
fi

echo Create and upload buildcache
if [ ${UPLOAD_BUILDCACHE-x} = "true" ]; then
  echo Prepare mirror and buildcache
  # TODO: push gpg key to mirror (broken in 0.17, should be working in 0.18)
  ${WORKSPACE}/spack/bin/spack -e ${SPACK_ENV_NAME} buildcache create -r -a -f --mirror-url s3://cms-spack/${SCRAM_ARCH}/
  scp ${WORKSPACE}/spack/var/spack/environments/${SPACK_ENV_NAME}/spack.lock lxplus:/eos/user/r/razumov/www/CMS/environment/spack-${SPACK_ENV_NAME}-${SCRAM_ARCH}.lock
fi
echo build.sh done
