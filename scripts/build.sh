#!/bin/bash -x
# Retry a command with exponential backoff
# Source: https://gist.github.com/askoufis/0da8502b5f1df4d067502273876fcd07
function retry {
  local maxAttempts=$1
  local secondsDelay=1
  local attemptCount=1
  local output=
  shift 1

  while [ $attemptCount -le $maxAttempts ]; do
    output=$("$@")
    local status=$?

    if [ $status -eq 0 ]; then
      break
    fi

    if [ $attemptCount -lt $maxAttempts ]; then
      echo "Command [$@] failed after attempt $attemptCount of $maxAttempts. Retrying in $secondsDelay second(s)." >&2
      sleep $secondsDelay
    elif [ $attemptCount -eq $maxAttempts ]; then
      echo "Command [$@] failed after $attemptCount attempt(s)" >&2
      return $status;
    fi
    attemptCount=$(( $attemptCount + 1 ))
    secondsDelay=$(( $secondsDelay * 2 ))
  done

  echo $output
}

SSH_OPTS="-o StrictHostKeyChecking=no -o GSSAPIAuthentication=yes -o GSSAPIDelegateCredentials=yes"

[ -z ${WORKSPACE+x} ] && (echo 'ERROR: WORKSPACE not set, quitting'; exit 1)
[ -z ${RPM_INSTALL_PREFIX+x} ] && (echo 'ERROR: RPM_INSTALL_PREFIX not set, quitting'; exit 2)
[ -z ${SPACK_ENV_NAME+x} ] && (echo 'ERROR: SPACK_ENV_NAME not set, quitting'; exit 3)
[ -z ${SCRAM_ARCH+x} ] && (echo 'ERROR: SCRAM_ARCH not set, quitting'; exit 4)

if [ `uname` == "Darwin" ]; then
    CORES=`sysctl -n hw.ncpu`
elif [ `uname` == "Linux" ]; then
    CORES=`awk '/^processor/ { N++} END { print N }' /proc/cpuinfo`
fi
export CORES
echo Setup Spack for CMS
cd $WORKSPACE

# For boto3
export PYTHONPATH=/cvmfs/cms-ib.cern.ch/share/python3/lib/python3.6/site-packages:$PYTHONPATH

export S3_ENDPOINT_URL=https://s3.cern.ch
export SPACK_DISABLE_LOCAL_CONFIG=true
export SPACK_USER_CACHE_PATH=$WORKSPACE
cd spack
echo Add signing key
if [ ! -z ${SPACK_GPG_KEY+x} ]; then
  if [ -e ${SPACK_GPG_KEY} ]; then
    bin/spack gpg trust $SPACK_GPG_KEY
  else
    echo ERROR: GPG key not found
    touch ${WORKSPACE}/fail
    exit 1
  fi
fi

SPACK_DEBUG_FLAG=""
if [ ! -z ${SPACK_DEBUG+x} ]; then
  SPACK_DEBUG_FLAG="-d --stacktrace"
fi

echo Setup spack
. share/spack/setup-env.sh
echo Add padding to install_tree
${WORKSPACE}/spack/bin/spack ${SPACK_DEBUG_FLAG} -e ${SPACK_ENV_NAME} config add "config:install_tree:root:${RPM_INSTALL_PREFIX}"
${WORKSPACE}/spack/bin/spack ${SPACK_DEBUG_FLAG} -e ${SPACK_ENV_NAME} config add "config:install_tree:padded_length:128"
echo Start the installation
${WORKSPACE}/spack/bin/spack ${SPACK_DEBUG_FLAG} -e ${SPACK_ENV_NAME} concretize --fresh -f
if [ $? -ne 0 ]; then
    echo Concretization failed
    touch $WORKSPACE/fail
    exit 1
fi

${WORKSPACE}/spack/bin/spack ${SPACK_DEBUG_FLAG} -e ${SPACK_ENV_NAME} install --fresh --show-log-on-error -j$CORES --fail-fast
exit_code=$?
if [ ${exit_code} -ne 0 ]; then
    echo Build failed, uploading logs
    ssh $SSH_OPTS cmsbuild@lxplus rm -rf /eos/user/r/razumov/www/CMS/logs/${SPACK_ENV_NAME}-${SCRAM_ARCH}
    ssh $SSH_OPTS cmsbuild@lxplus mkdir /eos/user/r/razumov/www/CMS/logs/${SPACK_ENV_NAME}-${SCRAM_ARCH}
    pushd ${WORKSPACE}/spack/stage
    find . -maxdepth 1 -type d -name 'spack-stage-*' -print0 | while read -d $'\0' dirn
    do
        ssh $SSH_OPTS cmsbuild@lxplus mkdir /eos/user/r/razumov/www/CMS/logs/${SPACK_ENV_NAME}-${SCRAM_ARCH}/$dirn
        scp $SSH_OPTS $dirn/*.txt cmsbuild@lxplus:/eos/user/r/razumov/www/CMS/logs/${SPACK_ENV_NAME}-${SCRAM_ARCH}/$dirn
    done
    popd
    scp $SSH_OPTS ${WORKSPACE}/spack/var/spack/environments/${SPACK_ENV_NAME}/spack.lock cmsbuild@lxplus:/eos/user/r/razumov/www/CMS/logs/${SPACK_ENV_NAME}-${SCRAM_ARCH}/
    touch $WORKSPACE/fail
#    exit ${exit_code}
fi

echo Create and upload buildcache
if [ ${UPLOAD_BUILDCACHE-x} = "true" ]; then
  echo Prepare mirror and buildcache
  # TODO: push gpg key to mirror (broken in 0.17, should be working in 0.18)
  ${WORKSPACE}/spack/bin/spack -e ${SPACK_ENV_NAME} buildcache create -r -a --mirror-url s3://cms-spack/${SCRAM_ARCH}/${SPACK_ENV_NAME}
  scp ${WORKSPACE}/spack/var/spack/environments/${SPACK_ENV_NAME}/spack.lock lxplus:/eos/user/r/razumov/www/CMS/environment/spack-${SPACK_ENV_NAME}-${SCRAM_ARCH}.lock
fi
echo build.sh done
exit ${exit_code}
