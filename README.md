# ceph and openstack on centos using ansible
ansible deploy for redhat ceph and openstack mitaka on centos7

thing to do before using this ansible project:
- set correct info in staging/inventory or production/inventory file and use that for inventory of hosts. use staging/inventory.example as template
- set correct defaults in group_vars/all/main.yml. use examples/group_vars_all_example as template
- set passwords in roles/openstack-common/vars/passwords.yml or roles/openstack-common/vars/passwords_[cluster].yml
  use roles/openstack-common/vars/passwords.yml.example as example
- setup ssh known hosts (might use 'ansible -i ./inventory all -m setup' for that)
- start out with 4 nodes (1 as mon and 3 as osd) using default centos7 deploy (base image, nothing special)
- use this playbook to setup nodes as needed. This basically does everything that is written down in 
  http://docs.ceph.com/docs/master/start/quick-start-preflight/
- after that it will do all the stuff to create a ceph cluster
- after that you can expand, or create a new cluster with more nodes

Please be aware that this playbook has been developed using ansible 2.1.0.0.

At this moment I am extending this project to add a openstack mitaka deployment.
