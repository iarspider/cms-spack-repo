#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

mkdir -p ${RPM_INSTALL_PREFIX}/common ${RPM_INSTALL_PREFIX}/etc/cms-git-tools ${RPM_INSTALL_PREFIX}/share/man/man1

#Check if a newer revision is already installed
if [ -f ${RPM_INSTALL_PREFIX}/etc/cms-git-tools/version ] ; then
  oldrev=$(cat ${RPM_INSTALL_PREFIX}/etc/cms-git-tools/version )
  if [ ${oldrev} -ge %{fakerevision} ] ; then
    exit 0
  fi
fi

for file in $(find . -name '*' -type f -path '*/common/*' -o -type f -path '*/share/*') ; do
  cp -f ${file} ${RPM_INSTALL_PREFIX}/${file}
done
for file in $(find . -name '*' -type l -path '*/common/*') ; do
  cp -pRf ${file} ${RPM_INSTALL_PREFIX}/${file}
done
rm -f ${RPM_INSTALL_PREFIX}/common/git-addpkg
rm -f ${RPM_INSTALL_PREFIX}/common/git-checkdeps

echo %{fakerevision} > ${RPM_INSTALL_PREFIX}/etc/cms-git-tools/version
