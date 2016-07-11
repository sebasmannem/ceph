#!/bin/bash
ceph osd tree | sed -n '/host '$(hostname)'/,/host/p' | grep -Eo 'osd\.[0-9]+'
