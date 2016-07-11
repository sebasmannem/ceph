#!/bin/sh

set -e
PART=$(echo $1 | grep -o '[0-9]*$')
DISK=$(echo $1 | sed 's/[0-9]*$//')

blkid "$DISK$PART" | grep -q 'PARTLABEL="ceph data"' || exit 1
dd if=/dev/zero of=$DISK$PART bs=4096 count=256
parted -s $DISK rm $PART
rm -f $DISK$PART
