#!/usr/bin/env python2
import json

from subprocess import Popen, PIPE, check_call
import argparse

parser = argparse.ArgumentParser(description='Set keystone defaults for a new openstack deployment.')
parser.add_argument('-s', '--service', dest='service', help='name of service to create')
parser.add_argument('-t', '--servicetype', dest='servicetype', help='type of service to create')
parser.add_argument('-r', '--regions', dest='regions', default='RegionOne', help='list of regions (comma seperated) of regions to create')
parser.add_argument('-u', '--urls', dest='urls', help='list of urls (comma seperated) of urls to create. Example: admin=http://localhost:35357/v3,public=http://localhost:5000/v3,internal=http://localhost:5000/v3')
args = parser.parse_args()

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
openstack=Popen(["openstack", "service", "list", "--format", "json"], stdout=PIPE)
svcs = openstack.stdout.read()
svcs = json.loads(svcs)
existing_services = [ str(svc['Name']) for svc in svcs if svc['Type']==servicetype ]

if service not in existing_services:
    print("creating service {0}".format(service))
    check_call(["openstack", "service", "create", "--name", service, "--description", "OpenStack {0} service {1}".format(servicetype, service), servicetype])

print("checking for endpoint existence")
openstack=Popen(["openstack", "endpoint", "list", "--format", "json"], stdout=PIPE)
eps = openstack.stdout.read()
eps = json.loads(eps)
existing_regions = [ str(ep['Region']) for ep in eps if ep['Service Name'] == service ]

for region in regions:
    if region not in existing_regions:
        for endpoint, url in urls:
            print("creating {0} endpoint for region {1}".format(endpoint, region))
            check_call(["openstack", "endpoint", "create", "--region", region, servicetype, endpoint, url])
