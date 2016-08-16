#!/usr/bin/env python2
import json

from subprocess import Popen, PIPE, check_call
import socket

import argparse

parser = argparse.ArgumentParser(description='Set keystone defaults for a new openstack deployment.')
parser.add_argument('--adminpassword', dest='adminpassword', help='admin password')
parser.add_argument('--demopassword', dest='demopassword', help='demo password')

args = parser.parse_args()

print("checking for service existence")
openstack=Popen(["openstack", "service", "list", "--format", "json"], stdout=PIPE)
svcs = openstack.stdout.read()
svcs = json.loads(svcs)
ident_svcs = [ str(svc['Name']) for svc in svcs if svc['Type']=='identity' ]

if 'keystone' not in ident_svcs:
    print("creating keystone service")
    check_call(["openstack", "service", "create", "--name", "keystone", "--description", "OpenStack Identity", "identity"])

print("checking for endpoint existence")
openstack=Popen(["openstack", "endpoint", "list", "--format", "json"], stdout=PIPE)
eps = openstack.stdout.read()
eps = json.loads(eps)
keystone_eps = [ str(ep['Region']) for ep in eps if ep['Service Name']=='keystone' ]

if "RegionOne" not in keystone_eps:
    print("creating keystone endpoints")
    check_call(["openstack", "endpoint", "create", "--region", "RegionOne", "identity", "public", "http://{0}:5000/v{1}".format(socket.gethostname(), args.apiversion)])
    check_call(["openstack", "endpoint", "create", "--region", "RegionOne", "identity", "internal", "http://{0}:5000/v{1}".format(socket.gethostname(), args.apiversion)])
    check_call(["openstack", "endpoint", "create", "--region", "RegionOne", "identity", "admin", "http://{0}:35357/v{1}".format(socket.gethostname(), args.apiversion)])

print("checking for domain existence")
openstack=Popen(["openstack", "domain", "list", "--format", "json"], stdout=PIPE)
ds = openstack.stdout.read()
ds = json.loads(ds)
domain_names = [ str(d['Name']) for d in ds ]

if "default" not in domain_names:
    print("creating default domain")
    check_call(["openstack", "domain", "create", "--description", "Default Domain", "default"])

print("checking for project existence")
openstack=Popen(["openstack", "project", "list", "--format", "json"], stdout=PIPE)
ps = openstack.stdout.read()
ps = json.loads(ps)
project_names = [ str(p['Name']) for p in ps ]


for u in ['admin', 'service', 'demo']:
    if u not in project_names:
        print("creating {0} project".format(u))
        check_call(["openstack", "project", "create", "--domain", "default", "--description", "{0} Project".format(u.capitalize()), u])

print("checking for user existence")
openstack=Popen(["openstack", "user", "list", "--format", "json"], stdout=PIPE)
us = openstack.stdout.read()
us = json.loads(us)
user_names = [ str(u['Name']) for u in us ]

if "admin" not in user_names:
    print("creating admin user")
    check_call(["openstack", "user", "create", "--domain", "default", "--password", str(args.adminpassword), "admin"])
if "demo" not in user_names:
    print("creating demo user")
    check_call(["openstack", "user", "create", "--domain", "default", "--password", str(args.demopassword), "demo"])

print("checking for role existence")
openstack=Popen(["openstack", "role", "list", "--format", "json"], stdout=PIPE)
rs = openstack.stdout.read()
rs = json.loads(rs)
role_names = [ str(r['Name']) for r in rs ]

for r in ['admin', 'user']:
    if r not in role_names:
        print("creating {0} role".format(r))
        check_call(["openstack", "role", "create", r])

print("adding admin role to admin user for admin project")
check_call(["openstack", "role", "add", "--project", "admin", "--user", "admin", "admin"])

print("adding user role to demo user for demo project")
check_call(["openstack", "role", "add", "--project", "demo", "--user", "demo", "user"])

