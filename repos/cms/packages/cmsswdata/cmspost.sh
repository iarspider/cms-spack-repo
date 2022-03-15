#!/bin/bash -xe
BaseTool=""
directpkgreqs=""
prefix=""
### END CONFIG

echo "${BaseTool}_ROOT='$prefix'" > prefix/etc/profile.d/init.sh
echo "set ${BaseTool}_ROOT='$prefix'" > prefix/etc/profile.d/init.csh
echo "${BaseTool}_PKGREQUIRED='$directpkgreqs'" >> prefix/etc/profile.d/init.sh
echo "set ${BaseTool}_PKGREQUIRED='$directpkgreqs'" >> prefix/etc/profile.d/init.csh

for DATA_PATH in $directpkgreqs; do
  PKG_DIR=$(echo $DATA_PATH | cut -d/ -f2)
  [ $(echo $PKG_DIR | grep '^data-' | wc -l) -eq 1 ] || continue
  PKG_DIR=$(echo $PKG_DIR | sed 's|^data-||;s|-|/|')
  SOURCE=$prefix/$DATA_PATH
  DES_PATH=$(echo $DATA_PATH | cut -d/ -f1,2)/$(echo $DATA_PATH | cut -d/ -f3 | tr '-' '\n' | grep '^V[0-9][0-9]$\|^[0-9][0-9]$' | tr '\n' '-' | sed 's|-$||')
  PKG_DATA=$(echo $PKG_DIR | cut -d/ -f1)
  if [ ! -e $RPM_INSTALL_PREFIX/share/$DES_PATH/$PKG_DIR ] ; then
    rm -rf $RPM_INSTALL_PREFIX/share/$DES_PATH
    mkdir -p $RPM_INSTALL_PREFIX/share/$DES_PATH
    if [ -L $SOURCE/$PKG_DATA ] ; then
      ln -fs $prefix/$DATA_PATH/$PKG_DATA $RPM_INSTALL_PREFIX/share/$DES_PATH/$PKG_DATA
    else
      echo "Moving $DATA_PATH in share"
      rsync -aq --no-t --size-only $SOURCE/$PKG_DATA/ $RPM_INSTALL_PREFIX/share/$DES_PATH/$PKG_DATA/
    fi
  fi
  if [ ! -L $SOURCE/$PKG_DATA ] ; then
    rm -rf $SOURCE/$PKG_DATA && ln -fs $RPM_INSTALL_PREFIX/share/$DES_PATH/$PKG_DATA/ $SOURCE/$PKG_DATA
  fi
done
