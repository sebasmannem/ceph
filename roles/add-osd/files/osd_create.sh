#!/bin/bash
set -x
set -e
cd /dev

DISK=$1
[ "$DISK" ] || exit 1

OSDNUM=$(ceph osd create)
sudo -u ceph mkdir /var/lib/ceph/osd/ceph-$OSDNUM
mount ${DISK}1 /var/lib/ceph/osd/ceph-$OSDNUM
