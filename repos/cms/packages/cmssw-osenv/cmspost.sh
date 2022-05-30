#!/bin/bash
pkgname=""
fakerevision=""
## END CONFIG

pkgrel=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd ${pkgrel}
mkdir -p ${RPM_INSTALL_PREFIX}/common ${RPM_INSTALL_PREFIX}/etc/${pkgname}

#Check if a newer revision is already installed
if [ -f ${RPM_INSTALL_PREFIX}/etc/${pkgname}/version ] ; then
  oldrev=$(cat ${RPM_INSTALL_PREFIX}/etc/${pkgname}/version )
  if [ ${oldrev} -ge ${fakerevision} ] ; then
    exit 0
  fi
fi

for file in $(find . -name '*' -type f -path '*/common/*') ; do
  cp -f ${file} ${RPM_INSTALL_PREFIX}/${file}
done
for file in $(find . -name '*' -type l -path '*/common/*') ; do
  cp -pRf ${file} ${RPM_INSTALL_PREFIX}/${file}
done

echo ${fakerevision} > ${RPM_INSTALL_PREFIX}/etc/${pkgname}/version
