#!/usr/bin/env python2
import json

from subprocess import Popen, PIPE, check_call
import socket

import argparse

parser = argparse.ArgumentParser(description='Create keystone domain, users, projects, roles and add roles to users in projects as needed.')
parser.add_argument('-d', '--domain', dest='domain', default='default', help='user domain')
parser.add_argument('-u', '--user', dest='user', help='user name')
parser.add_argument('-p', '--password', dest='password', help='user password')
parser.add_argument('-r', '--roles', dest='role', default='', help='list of roles for user in projects. Format project1:role1,project2:role2')

args = parser.parse_args()

domain = args.domain.lower()
user = args.user.lower()

# Generate list of tuples [ ( 'project1', 'role1' ), ('project2', 'role2' ) ]
# Use variabele as startpoint
project_roles = args.roles
# But lowercase
project_roles = project_roles.lower()
# And without spaces
project_roles = project_roles.replace(' ', '')
# split in list of elements by comma
project_roles = project_roles.split(',')
# split in list of tuples ( project, role) when item has one colon
project_roles = [ tuple(r.split(':')) for r in project_roles if r.count(':') == 1 ]

# capture all projects (unique set of first item in every tuple)
projects = set([ r[0] for r in project_roles ])

# capture all projects (unique set of second item in every tuple)
roles = set([ r[1] for r in project_roles ])

print("checking for domain existence")
openstack=Popen(["openstack", "domain", "list", "--format", "json"], stdout=PIPE)
ds = openstack.stdout.read()
ds = json.loads(ds)
existing_domains = [ str(d['Name']) for d in ds ]

if domain not in existing_domains:
    print("creating domain {0}".format(domain))
    check_call(["openstack", "domain", "create", "--description", "{0} domain".format(domain.capitalize()), domain])

print("checking for project existence")
openstack=Popen(["openstack", "project", "list", "--format", "json"], stdout=PIPE)
ps = openstack.stdout.read()
ps = json.loads(ps)
existing_projects = [ str(p['Name']) for p in ps ]

for project in projects:
    if project not in existing_projects:
        print("creating project {0}".format(project))
        check_call(["openstack", "project", "create", "--domain", domain, "--description", "{0} project".format(project.capitalize()), project])

print("checking for user existence")
openstack=Popen(["openstack", "user", "list", "--format", "json"], stdout=PIPE)
us = openstack.stdout.read()
us = json.loads(us)
existing_users = [ str(u['Name']).lower() for u in us ]

if user not in user_names:
    print("creating user {0}".format(user))
    check_call(["openstack", "user", "create", "--domain", domain, "--password", str(args.password), user])

print("checking for role existence")
openstack=Popen(["openstack", "role", "list", "--format", "json"], stdout=PIPE)
rs = openstack.stdout.read()
rs = json.loads(rs)
existing_roles = [ str(r['Name']) for r in rs ]

for role in roles:
    if role not in existing_roles:
        print("creating role {0}".format(role))
        check_call(["openstack", "role", "create", role])

for project, role in project_roles:
    print("adding {0} role to {1} user for {2} project".format(role, user, project))
    check_call(["openstack", "role", "add", "--project", project, "--user", user, role])

