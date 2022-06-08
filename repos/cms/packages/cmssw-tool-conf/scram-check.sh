#!/bin/bash
if [ -e $SCRAMV1_ROOT/bin/chktool ] ; then
  touch $1/errors.log
  find $1/tools -name '*.xml' -type f | (xargs $SCRAMV1_ROOT/bin/chktool >> $1/errors.log 2>&1 || true)
  if [ $(grep 'ERROR:' $1/errors.log | wc -l) -gt 0 ] ; then
    cat $1/errors.log
    exit 1
  fi
  rm -f $1/errors.log
fi
