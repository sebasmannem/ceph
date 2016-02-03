# ceph
ansible deploy for redhat ceph on centos7

thing to consider:
- set correct info in staging/inventory or production/inventory file and use that for inventory of hosts
- for test: add the ip of your KVM bridge (e.a. virbr0 192.168.122.1) to /etc/resolv.conf for dns resolution of spinned VM's
- setup ssh known hosts (might use 'ansible -i ./inventory all -m setup' for that)
- create 4 nodes using default centos7 deploy (base image, nothing special)
- use this playbook to setup nodes as needed. This basically does everything taht is written down in 
  http://docs.ceph.com/docs/master/start/quick-start-preflight/
- then you can go ahead doing the stuff that is written in 
  http://docs.ceph.com/docs/master/start/quick-ceph-deploy/
  and have some fun.

Please be aware that this playbook has been developed using ansible 1.9.4.
I will test it with ansible 2.0.0.2 shortly.
And I will extend it to add the stuff from http://docs.ceph.com/docs/master/start/quick-ceph-deploy/ to get a fully running cluster.
I might extend it to use RH servers also. ANd I might extend it to let ansible do all the deploy stuff (instead of ceph-installdoing some heavy lifting).
But for now, enjoy...
