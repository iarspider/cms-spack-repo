#!/bin/bash
OLD_REV=0
if [ -f $2 ] ; then OLD_REV=$(grep '^\s*#\s*CMSDIST_FILE_REVISION\s*=' $2 | tail -1 | sed 's|.*=||;s| ||g') ; fi
NEW_REV=$(grep '^\s*#\s*CMSDIST_FILE_REVISION\s*=' $1 | tail -1 | sed 's|.*=||;s| ||g')
if [ ${OLD_REV} -lt ${NEW_REV} ] ; then rm -f $2 ; cp $1 $2 ; fi


