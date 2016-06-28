#!/bin/sh
set -e
OSDNUM=$1
[ "$OSDNUM" -ge 0 ] || exit 1
DISK=$(mount | sed -nr '/\/var\/lib\/ceph\/osd\/ceph-'$OSDNUM'/{s|(/dev/[a-z]+)[0-9]+ on /var/lib/ceph/osd/ceph-[0-9]+ .*|\1|;p}')

umount "/var/lib/ceph/osd/ceph-$OSDNUM"
UUID=$(blkid ${DISK}1 -o export | grep -E '^UUID=')
cp /etc/fstab /tmp/fstab.$(date +%s)
[ "$UUID" ] && sed -i "/^$UUID/d" /etc/fstab

# First: use parted to find partitions
parted $DISK -s -m print | awk 'BEGIN{FS=":"}/^[1-9]/{print $1}' | while read PART; do
  # For every partition: write 1M empty blocks
  dd if=/dev/zero of=$DISK$PART bs=4096 count=256
  parted -s $DISK rm $PART
  rm -f $DISK$PART
done

# Remove partitiontable (replace by empty one)
parted -s $DISK mklabel gpt

#from this point ceph-disk zap will work fine, so you can reuse this disk...
