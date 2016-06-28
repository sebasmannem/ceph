#!/bin/bash
set -e
cd /dev

DISK=$1
[ "$DISK" ] || exit 1

PARTS=$(parted $DISK -s -m print | awk 'BEGIN{FS=":"}/^[1-9]/{print $1}')
if [ "$PARTS" ]; then
  echo "$DISK still has partitions:"
  echo "$PARTS" | while read PART; do
    echo $DISK$PART
  done
  exit 1
fi

parted -s $DISK -- 'mklabel gpt mkpart "ceph data" xfs 1 -1'
mkfs.xfs ${DISK}1

OSDNUM=$(ceph osd create)
sudo -u ceph mkdir /var/lib/ceph/osd/ceph-$OSDNUM
mount ${DISK}1 /var/lib/ceph/osd/ceph-$OSDNUM
chown ceph:ceph /var/lib/ceph/osd/ceph-$OSDNUM

sudo -u ceph ceph-osd -i $OSDNUM --mkfs --mkkey

ceph auth add osd.$OSDNUM osd 'allow *' mon 'allow rwx' -i /var/lib/ceph/osd/ceph-$OSDNUM/keyring

ceph osd crush add osd.$OSDNUM 1.0 host=$(hostname)

systemctl enable ceph-osd@$OSDNUM
systemctl start ceph-osd@$OSDNUM
