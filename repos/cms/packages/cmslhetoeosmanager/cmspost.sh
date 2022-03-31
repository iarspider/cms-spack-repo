#!/bin/bash
#Check if a newer revision is already installed
if [ -f ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/version ] ; then
  if [ $(cat ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/version) -ge %{realversion} ] ; then
    exit 0
  fi
fi

mkdir -p $RPM_INSTALL_PREFIX/share/overrides/bin ${RPM_INSTALL_PREFIX}/etc/%{pkgname}
cp %{prefix}/cmsLHEtoEOSManager.py $RPM_INSTALL_PREFIX/share/overrides/bin
echo %{realversion} > ${RPM_INSTALL_PREFIX}/etc/%{pkgname}/version
