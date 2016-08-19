#!/usr/bin/env python2
import json
import os
import re

from subprocess import Popen, PIPE, check_call
import argparse

parser = argparse.ArgumentParser(description='Set keystone defaults for a new openstack deployment.')
parser.add_argument('-s', '--service', dest='service', help='name of service to create')
parser.add_argument('-t', '--servicetype', dest='servicetype', help='type of service to create')
parser.add_argument('-r', '--regions', dest='regions', default='RegionOne', help='list of regions (comma seperated) of regions to create')
parser.add_argument('-u', '--urls', dest='urls', help='list of urls (comma seperated) of urls to create. Example: admin=http://localhost:35357/v3,public=http://localhost:5000/v3,internal=http://localhost:5000/v3')
parser.add_argument('-o', '--openrc', dest='openrc', default='', help='openrc file with credentials to openstack')
args = parser.parse_args()

#Find all environment variablen starting with 'OS_'
env = dict([ (k, v) for k, v in os.environ.items() if k[:3] == 'OS_' ])

#Add all exported variablen in args.openrc file
env_re = re.compile('^\s*export\s+(\S+)=(.*)$')
if args.openrc:
    openrc = os.path.expanduser(args.openrc)
    with open(openrc, 'r') as f:
        for line in f:
            line = line.rstrip()
            m = env_re.search(line)
            if m:
                k, v = m.groups()
                if k[:3] == 'OS_':
                    env[k] = v
#env should now contain everything needed for openstack command to operate as needed

service = args.service.lower()
servicetype = args.servicetype.lower()
regions = args.regions.split(',')

#generate dictionary of urls
# Use variabele as startpoint
urls = args.urls
# split in list of elements by comma
urls = urls.split(',')
# split in list of tuples ( project, role) when item has one colon
urls = dict([ tuple(u.split('=')) for u in urls if u.count('=') == 1 ])

print("checking for service existence")
openstack=Popen(["openstack", "service", "list", "--format", "json"], stdout=PIPE, env=env)
svcs = openstack.stdout.read()
svcs = json.loads(svcs)
existing_services = [ str(svc['Name']) for svc in svcs if svc['Type']==servicetype ]

if service not in existing_services:
    print("creating service {0}".format(service))
    check_call(["openstack", "service", "create", "--name", service, "--description", "OpenStack {0} service {1}".format(servicetype, service), servicetype], env=env)

print("checking for endpoint existence")
openstack=Popen(["openstack", "endpoint", "list", "--format", "json"], stdout=PIPE, env=env)
eps = openstack.stdout.read()
eps = json.loads(eps)
existing_regions = [ str(ep['Region']) for ep in eps if ep['Service Name'] == service ]

for region in regions:
    if region not in existing_regions:
        for endpoint, url in urls.items():
            print("creating {0} endpoint for region {1}".format(endpoint, region))
            check_call(["openstack", "endpoint", "create", "--region", region, servicetype, endpoint, url], env=env)
