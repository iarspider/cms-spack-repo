#!/bin/bash -xe
if [ `uname` == "Darwin" ]; then
	CORES=`sysctl -n hw.ncpu`
elif [ `uname` == "Linux" ]; then
	CORES=`awk '/^processor/ { N++} END { print N }' /proc/cpuinfo`
fi
export CORES
echo Setup Spack for CMS
cd $WORKSPACE/cms-spack-repo
bash -xe ./bootstrap.sh
cd spack
source share/spack/setup-env.sh 
echo Add signing key
spack gpg trust $SPACK_GPG_KEY
echo Start the installation
spack env activate CMSSW_12_0_X
spack install -j$CORES --fail-fast
echo Prepare mirror and buildcache
spack mirror create -d $WORKSPACE/mirror --all --dependencies
spack buildcache create -r -f -a -d $WORKSPACE/mirror
spack gpg publish -d $WORKSPACE/mirror --rebuild-index
cd $WORKSPACE
echo Upload mirror
rsync -e "ssh -o StrictHostKeyChecking=no -o GSSAPIAuthentication=yes -o GSSAPIDelegateCredentials=yes" --recursive --links --ignore-existing mirror/ cmsbuild@lxplus:/eos/user/r/razumov/www/CMS/mirror
echo Done