#!/bin/bash
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
cd spack
# source share/spack/setup-env.sh
echo Add signing key
if [ ! -z ${SPACK_GPG_KEY+x} ]; then bin/spack gpg trust $SPACK_GPG_KEY; fi
echo Add padding to install_tree
bin/spack config add "config:install_tree:padded_length:128"
echo Start the installation
# bin/spack env activate ${SPACK_ENV_NAME}
bin/spack -e ${SPACK_ENV_NAME} -d --show-cores=minimized concretize
SPACK_MON_ARGS=""
SPACKMON_USER="cmsbuild"
if [ ! -z ${SPACKMON_TOKEN} ]; then SPACK_MON_ARGS="--monitor --monitor-host http://cms-spackmon.cern.ch/cms-spackmon"; fi;
bin/spack -e ${SPACK_ENV_NAME} -d install -j$CORES --fail-fast $SPACK_MON_ARGS
echo Prepare mirror and buildcache
bin/spack -e ${SPACK_ENV_NAME} mirror create -d $WORKSPACE/mirror --all --dependencies
if [ ${UPLOAD_BUILDCACHE-x} = "true" ]; then
  bin/spack -e ${SPACK_ENV_NAME} buildcache create -r -f -a -d $WORKSPACE/mirror
  bin/spack -e ${SPACK_ENV_NAME} gpg publish -d $WORKSPACE/mirror --rebuild-index
  cd $WORKSPACE
  echo Upload mirror
  rsync -e "ssh -o StrictHostKeyChecking=no -o GSSAPIAuthentication=yes -o GSSAPIDelegateCredentials=yes" --recursive --links --ignore-existing mirror/ cmsbuild@lxplus:/eos/user/r/razumov/www/CMS/mirror
fi
echo Done
