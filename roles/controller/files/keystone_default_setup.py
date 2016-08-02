#!/usr/bin/env python2
import json

from subprocess import Popen, PIPE, check_call
import socket

import ConfigParser
import os
try:
    config = ConfigParser.ConfigParser()
    config.readfp(open('/etc/keystone/keystone.conf'))
    default_token = config.get('DEFAULT', 'admin_token')
except:
    default_token = ''

import os
try:
    default_token = os.environ['OS_TOKEN']
except:
    pass

try:
    default_apiversion = os.environ['OS_IDENTITY_API_VERSION']
except:
    default_apiversion = 3

try:
    default_url = os.environ['OS_URL']
except:
    default_url = 'http://{0}:35357/v{1}'.format(socket.gethostname(), default_apiversion)

import argparse

parser = argparse.ArgumentParser(description='Set keystone defaults for a new openstack deployment.')
parser.add_argument('-t', '--token', dest='token', default=default_token, help='OS_TOKEN')
parser.add_argument('-u', '--url', dest='url', default=default_url, help='OS_URL')
parser.add_argument('-a', '--apiversion', dest='apiversion', default=default_apiversion, help='OS_IDENTITIY_API_VERSION')
parser.add_argument('-p', '--password', dest='password', help='admin password')

args = parser.parse_args()

env={"OS_TOKEN": args.token, "OS_URL": args.url, "OS_IDENTITY_API_VERSION": str(args.apiversion) }

print("checking for service existence")
openstack=Popen(["openstack", "service", "list", "--format", "json"], env=env, stdout=PIPE)
svcs = openstack.stdout.read()
svcs = json.loads(svcs)
ident_svcs = [ str(svc['Name']) for svc in svcs if svc['Type']=='identity' ]

if 'keystone' not in ident_svcs:
    print("creating keystone service")
    check_call(["openstack", "service", "create", "--name", "keystone", "--description", "OpenStack Identity", "identity"], env=env)

print("checking for endpoint existence")
openstack=Popen(["openstack", "endpoint", "list", "--format", "json"], env=env, stdout=PIPE)
eps = openstack.stdout.read()
eps = json.loads(eps)
keystone_eps = [ str(ep['Region']) for ep in eps if ep['Service Name']=='keystone' ]

if "RegionOne" not in keystone_eps:
    print("creating keystone endpoints")
    check_call(["openstack", "endpoint", "create", "--region", "RegionOne", "identity", "public", "http://{0}:5000/v{1}".format(socket.gethostname(), args.apiversion)], env=env)
    check_call(["openstack", "endpoint", "create", "--region", "RegionOne", "identity", "internal", "http://{0}:5000/v{1}".format(socket.gethostname(), args.apiversion)], env=env)
    check_call(["openstack", "endpoint", "create", "--region", "RegionOne", "identity", "admin", "http://{0}:35357/v{1}".format(socket.gethostname(), args.apiversion)], env=env)

print("checking for domain existence")
openstack=Popen(["openstack", "domain", "list", "--format", "json"], env=env, stdout=PIPE)
ds = openstack.stdout.read()
ds = json.loads(ds)
domain_names = [ str(d['Name']) for d in ds ]

if "default" not in domain_names:
    print("creating default domain")
    check_call(["openstack", "domain", "create", "--description", "Default Domain", "default"], env=env)

print("checking for project existence")
openstack=Popen(["openstack", "project", "list", "--format", "json"], env=env, stdout=PIPE)
ps = openstack.stdout.read()
ps = json.loads(ps)
project_names = [ str(p['Name']) for p in ps ]


for u in ['admin', 'service', 'demo']:
    if u not in project_names:
        print("creating {0} project".format(u))
        check_call(["openstack", "project", "create", "--domain", "default", "--description", "{0} Project".format(u.capitalize()), u], env=env)

print("checking for user existence")
openstack=Popen(["openstack", "user", "list", "--format", "json"], env=env, stdout=PIPE)
us = openstack.stdout.read()
us = json.loads(us)
user_names = [ str(u['Name']) for u in us ]

if "admin" not in user_names:
    print("creating admin user")
    check_call(["openstack", "user", "create", "--domain", "default", "--password", str(args.password), "admin"], env=env)
if "demo" not in user_names:
    print("creating demo user")
    check_call(["openstack", "user", "create", "--domain", "default", "--password", "demo", "demo"], env=env)

print("checking for role existence")
openstack=Popen(["openstack", "role", "list", "--format", "json"], env=env, stdout=PIPE)
rs = openstack.stdout.read()
rs = json.loads(rs)
role_names = [ str(r['Name']) for r in rs ]

for r in ['admin', 'user']:
    if r not in role_names:
        print("creating {0} role".format(r))
        check_call(["openstack", "role", "create", r], env=env)

print("adding admin role to admin user for admin project")
check_call(["openstack", "role", "add", "--project", "admin", "--user", "admin", "admin"], env=env)

print("adding user role to demo user for demo project")
check_call(["openstack", "role", "add", "--project", "demo", "--user", "demo", "user"], env=env)

