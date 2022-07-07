#!/bin/bash
pkgname="cms-common"
cmsplatf="ChAnGeMe"
pkgrevision="123zzz"
mkdir -p $RPM_INSTALL_PREFIX/etc/${pkgname}  $RPM_INSTALL_PREFIX/${cmsplatf}/etc/profile.d

pkgrel=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd ${pkgrel}/${pkgrevision}

#Check if a newer revision is already installed
#Also force installation if older revision has deleted cmsset_default.sh
if [ -f $RPM_INSTALL_PREFIX/cmsset_default.csh ] && [ -f $RPM_INSTALL_PREFIX/etc/${pkgname}/revision ] ; then
  oldrev=`cat $RPM_INSTALL_PREFIX/etc/${pkgname}/revision`
  if [ $oldrev -ge ${pkgrevision} ] ; then
    exit 0
  fi
fi

for file in $(find . -name '*'); do
  if [ -d $file ] ; then
    mkdir -p $RPM_INSTALL_PREFIX/$file
  else
    rm -f $RPM_INSTALL_PREFIX/$file
    cp -P $file $RPM_INSTALL_PREFIX/$file
    sed -ie "s#@CMS_PREFIX@#${RPM_INSTALL_PREFIX}#g" $file
  fi
done
echo ${pkgrevision} > $RPM_INSTALL_PREFIX/etc/${pkgname}/revision
