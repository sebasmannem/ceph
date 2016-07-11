#!/usr/bin/env python2

import subprocess
import re

blkid_re = re.compile('[a-zA-Z]+=".*?"')

def line2vals(l):
    cols = blkid_re.findall(l)
    ret = {}
    ret['DEVICE'] = l.split(' ')[0][:-1]
    for c in cols:
        k,v = c.split('=')
        v = v[1:][:-1]
        ret[k] = v
    return ret

def blkdevs():
    sp = subprocess.Popen(['blkid'], stdout=subprocess.PIPE)
    for l in sp.stdout:
        yield line2vals(l.strip())

fstab_re = re.compile('UUID=\S+')
known_parts = set()
with open('/etc/fstab','r') as f:
    for l in f:
        dev=fstab_re.search(l)
        if dev:
            uuid=dev.group(0).split('=')[1]
            known_parts.add(uuid)

for d in blkdevs():
    try:
        if d['PARTLABEL'] != 'ceph data':
            continue
        elif 'TYPE' not in d:
            continue
        elif d['UUID'] in known_parts:
            continue
        else:
            print('UUID='+d['UUID'])
    except:
        pass
