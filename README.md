# ceph and openstack on centos using ansible
ansible deploy for redhat ceph and openstack mitaka on centos7

thing to do before using this ansible project:
- set correct info in staging/inventory or production/inventory file and use that for inventory of hosts
- setup ssh known hosts (might use 'ansible -i ./inventory all -m setup' for that)
- start out with 4 nodes using default centos7 deploy (base image, nothing special)
- use this playbook to setup nodes as needed. This basically does everything that is written down in 
  http://docs.ceph.com/docs/master/start/quick-start-preflight/
- after that het will do  all the stuff to create a ceph cluster

Please be aware that this playbook has been developed using ansible 2.1.0.0.

At this moment I am extending this project to add a openstack mitaka deployment.
And at this moment we are still having some puppet master doing stuff with finishing the servers.
I will change that to ansible playbook stuff too, so that this is an atomic end-to-end deployment.
