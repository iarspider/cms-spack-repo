#!/bin/bash
if [ $# -ne 1 ];
    then echo "Usage: run_chktool.sh <prefix>" && exit 1
fi
i=$1

touch ${i}/errors.log
find ${i}/tools -name '*.xml' -type f | (xargs $SCRAMV1_ROOT/bin/chktool >> ${i}/errors.log 2>&1 || true)
if [ $(grep 'ERROR:' ${i}/errors.log | wc -l) -gt 0 ] ; then
    cat ${i}/errors.log
    exit 1
fi
rm -f ${i}/errors.log