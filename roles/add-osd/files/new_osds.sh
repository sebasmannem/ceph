#!/bin/sh
#This sript will show all OSD's that are in $OSDDIR, but are not yet registered as a service.

OSDDIR=/var/lib/ceph/osd

#look for al folders in $OSDDIR
ls $OSDDIR | while read f; do
  # Check if it is already mounted
  mount | grep " on $OSDDIR/$f " > /dev/null || continue

  # extract OSD number from folder name
  OSDNUM=$(echo $f|grep -o -E '[0-9]+')

  #Check if it is already defined as a running service
  systemctl | grep -q "ceph-osd@$OSDNUM.service " && continue

  echo $OSDNUM
done
