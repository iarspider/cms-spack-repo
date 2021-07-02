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
# TODO: re-enable cache
spack install --no-cache -j$CORES --fail-fast
echo Prepare mirror and buildcache
spack mirror create -d $WORKSPACE/mirror --all --dependencies
spack buildcache create -r -f -a -d $WORKSPACE/mirror
cd $WORKSPACE
#export EOS_MGM_URL=root://eosuser.cern.ch
#mirrordate=$(date +%s%N)
#mirrorfile=mirror-${mirrordate}.tar
#tar -cf ../$mirrorfile *
#echo Transfer mirror
#xrdcp $mirrorfile root://eosuser.cern.ch//eos/user/r/razumov/CMS
#echo Unpack mirror
#xrdfs root://eosuser.cern.ch mkdir /eos/user/r/razumov/CMS/stage-$mirrordate
#ssh lxplus.cern.ch tar -C /eos/user/r/razumov/CMS/stage-$mirrordate -xf /eos/user/r/razumov/CMS/$mirrorfile
#ssh lxplus.cern.ch rsync --recursive --links --ignore-times --ignore-existing --size-only /eos/user/r/razumov/www/CMS/stage-$mirrordate/ /eos/user/r/razumov/CMS/mirror
echo Upload mirror
rsync -e "ssh -o StrictHostKeyChecking=no -o GSSAPIAuthentication=yes -o GSSAPIDelegateCredentials=yes" --recursive --links --ignore-existing mirror/ cmsbuild@lxplus:/eos/user/r/razumov/www/CMS/mirror
echo Done