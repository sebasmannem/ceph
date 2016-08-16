#!/usr/bin/env python2
import json

from subprocess import Popen, PIPE, check_call
import socket

import argparse

parser = argparse.ArgumentParser(description='Set glance defaults for a new openstack deployment.')
parser.add_argument('-p', '--password', dest='password', help='glance password')

args = parser.parse_args()

print("checking for service existence")
openstack=Popen(["openstack", "service", "list", "--format", "json"], stdout=PIPE)
svcs = openstack.stdout.read()
svcs = json.loads(svcs)
image_svcs = [ str(svc['Name']) for svc in svcs if svc['Type']=='image' ]

if 'glance' not in image_svcs:
    print("creating glance service")
    check_call(["openstack", "service", "create", "--name", "glance", "--description", "OpenStack Image", "image"])

print("checking for endpoint existence")
openstack=Popen(["openstack", "endpoint", "list", "--format", "json"], stdout=PIPE)
eps = openstack.stdout.read()
eps = json.loads(eps)
glance_eps = [ str(ep['Region']) for ep in eps if ep['Service Name']=='glance' ]

if "RegionOne" not in glance_eps:
    print("creating glance endpoints")
    check_call(["openstack", "endpoint", "create", "--region", "RegionOne", "identity", "public", "http://{0}:9292".format(socket.gethostname())])
    check_call(["openstack", "endpoint", "create", "--region", "RegionOne", "identity", "internal", "http://{0}:9292".format(socket.gethostname())])
    check_call(["openstack", "endpoint", "create", "--region", "RegionOne", "identity", "admin", "http://{0}:9292".format(socket.gethostname())])

print("checking for user existence")
openstack=Popen(["openstack", "user", "list", "--format", "json"], stdout=PIPE)
us = openstack.stdout.read()
us = json.loads(us)
user_names = [ str(u['Name']) for u in us ]

if "glance" not in user_names:
    print("creating glance user")
    check_call(["openstack", "user", "create", "--domain", "default", "--password", str(args.password), "glance"])

print("adding admin role to glance user for service project")
check_call(["openstack", "role", "add", "--project", "service", "--user", "glance", "admin"])
