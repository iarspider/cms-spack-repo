#!/bin/bash
# copy wrapper script into common if latest version is same as this version
mkdir -p $RPM_INSTALL_PREFIX/common
if [ "`ls ${RPM_INSTALL_PREFIX}/*/cms/das-client/v*/etc/profile.d/init.sh | sed 's|.*/cms/das-client/||;s|/etc/profile.d/init.sh||' | sort | tail -1`" = "%v" ] ; then
  /bin/cp -f ${RPM_INSTALL_PREFIX}/${pkgrel}/etc/das_client $RPM_INSTALL_PREFIX/common/das_client.tmp
  mv $RPM_INSTALL_PREFIX/common/das_client.tmp $RPM_INSTALL_PREFIX/common/das_client
fi

#Create overrides/bin directory (newly supported by SCRAM)
#and make sure that das_client.py script points to das_cleint wrapper
mkdir -p $RPM_INSTALL_PREFIX/share/overrides/bin
[ -e $RPM_INSTALL_PREFIX/share/overrides/bin/das_client.py ] || ln -sf ../../../common/das_client $RPM_INSTALL_PREFIX/share/overrides/bin/das_client.py 
