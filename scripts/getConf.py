#!/usr/bin/env python2
import ConfigParser
import os
import sys
import argparse
import re

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-f', '--filename', dest='filename', help='regexp for files to include.', default='.*')
parser.add_argument('-c', '--chapter', dest='chapter', help='chapter where the key should be', default='global')
parser.add_argument('-k', '--keyname', dest='key', help='chapter where the key should be')
parser.add_argument('rootdirs', nargs='+', help='folders to scan the ceph.conf files recide.')
args = parser.parse_args()

import ConfigParser

fsids = set()
filetester = re.compile(args.filename)

for rd in args.rootdirs:
    w=os.walk(rd)
    for dir, subdirs, files in w:
        for f in files:
            if not filetester.search(f):
                continue
            try:
                config = ConfigParser.RawConfigParser()
                config.read(os.path.join(dir, f))
                fsids.add(config.get(args.chapter,args.key))
            except:
                pass

for fsid in fsids:
    print(fsid)

sys.exit(len(fsids))
