#!/bin/bash

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

if [ -z ${SPACK_ENV_NAME} ]; then echo Please define ENV_SPACK_NAME; exit 1; fi
if [ `uname` == "Darwin" ]; then
	CORES=`sysctl -n hw.ncpu`
elif [ `uname` == "Linux" ]; then
	CORES=`awk '/^processor/ { N++} END { print N }' /proc/cpuinfo`
fi
export CORES
echo Setup Spack for CMS
cd $WORKSPACE/cms-spack-repo
[ ! -d spack ] && bash -xe ./bootstrap.sh
export SPACK_DISABLE_LOCAL_CONFIG=true
export SPACK_USER_CACHE_PATH=$WORKSPACE
cd spack
echo Add signing key
if [ ! -z ${SPACK_GPG_KEY+x} ]; then bin/spack gpg trust $SPACK_GPG_KEY; fi
echo Add padding to install_tree
bin/spack config add "config:install_tree:padded_length:128"
echo Set local monitor directory
bin/spack config add "config:monitor_dir:$WORKSPACE/monitor"
echo Start the installation
# bin/spack env activate ${SPACK_ENV_NAME}
# bin/spack -e ${SPACK_ENV_NAME} -d --show-cores=minimized concretize
SPACK_MON_ARGS=""
export SPACKMON_USER="cmsbuild"
if [ ! -z ${SPACKMON_TOKEN} ]; then SPACK_MON_ARGS="--monitor --monitor-save-local --monitor-tags ${SPACK_ENV_NAME}"; export SPACKMON_TOKEN; fi;
bin/spack --show-cores=minimized -e ${SPACK_ENV_NAME} -v install -j$CORES --fail-fast $SPACK_MON_ARGS
echo Upload monitor data
if [ ! -z ${SPACKMON_TOKEN} ]; then retry 5 bin/spack monitor --monitor-host http://cms-spackmon.cern.ch/cms-spackmon --monitor-keep-going --monitor-tags ${SPACK_ENV_NAME} upload $WORKSPACE/monitor; fi;
if [ ${UPLOAD_BUILDCACHE-x} = "true" ]; then
  echo Prepare mirror and buildcache
  bin/spack -e ${SPACK_ENV_NAME} mirror create -d $WORKSPACE/mirror --all --dependencies
  bin/spack -e ${SPACK_ENV_NAME} buildcache create -r -f -a -d $WORKSPACE/mirror
  bin/spack -e ${SPACK_ENV_NAME} gpg publish -d $WORKSPACE/mirror --rebuild-index
  cd $WORKSPACE
  echo Upload mirror
  rsync -e "ssh -o StrictHostKeyChecking=no -o GSSAPIAuthentication=yes -o GSSAPIDelegateCredentials=yes" --recursive --links --ignore-existing mirror/ cmsbuild@lxplus:/eos/user/r/razumov/www/CMS/mirror
fi
echo Done
