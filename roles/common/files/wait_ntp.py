#!/usr/bin/env python2
import subprocess
import argparse
import os
import re
import time

parser = argparse.ArgumentParser(description='Wait until time correct to within nn ms.')
parser.add_argument('-n', '--numsecs', dest='numsecs', type=int, help='Number of seconds time should be correct within.', default=100)
parser.add_argument('-d', '--delay', dest='delay', type=int, help='elay between two checks (ms).', default=1000)
parser.add_argument('-c', '--count', dest='count', type=int, help='Number of checks.', default=-1)
args = parser.parse_args()

time_re=re.compile('time correct to within (\d+) ms')
c=0
while True:
    ntpstat=subprocess.Popen(['ntpstat'], stdout=subprocess.PIPE)
    for l in ntpstat.stdout.readlines():
        try:
            m=time_re.search(l)
            num=m.group(1)
            if int(num) < args.numsecs:
                print("{0} < {1}".format(int(num),args.numsecs))
                os._exit(0)
        except:
            pass
    c+=1
    if c>args.count and args.count>=0:
        os._exit(1)
    print('Pass {0}'.format(c))
    time.sleep(float(args.delay)/1000)
