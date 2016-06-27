#!/bin/sh

WAIT_FOR_SECS=$1
: ${WAIT_FOR_SECS:=10}
EPOCH_UNTIL=$(($(date +%s) + $WAIT_FOR_SECS))
while [ $EPOCH_UNTIL -gt $(date +%s) ]; do
  /usr/bin/ceph health > /dev/null && exit 0
  echo -n "."
done
exit 1
