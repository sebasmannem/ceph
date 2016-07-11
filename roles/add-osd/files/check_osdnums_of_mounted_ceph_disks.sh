#!/bin/bash

# This script checks that whomai file tells same OSD num as where it is now mounnted.
# If this migth fail, one can use the input to fix, but for now, let's just leave it a check rather that a auto fix...
CLUSTER=$1
OSDNUM=$2
if [ -f "/var/lib/ceph/osd/${CLUSTER}-${OSDNUM}/whoami" ]; then
    WHOAMI=$(cat "/var/lib/ceph/osd/${CLUSTER}-${OSDNUM}/whoami")
    test "$OSDNUM" -eq "$WHOAMI"
fi
