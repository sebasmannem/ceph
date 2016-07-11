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

for d in blkdevs():
    try:
        if d['PARTLABEL'] != 'ceph data':
            continue
        elif 'TYPE' in d:
            continue
        else:
            print(d['DEVICE'])
    except:
        pass
