#!/usr/bin/env python2
import ConfigParser
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('rootdirs', nargs='+', help='folders to scan the ceph.conf files recide')
args = parser.parse_args()

import ConfigParser

fsids = set()

for rd in args.rootdirs:
    w=os.walk(rd)
    for dir, subdirs, files in w:
        for f in files:
            try:
                config = ConfigParser.RawConfigParser()
                config.read(os.path.join(dir, f))
                fsids.add(config.get('global','fsid'))
            except:
                pass

for fsid in fsids:
    print(fsid)

sys.exit(len(fsids))
