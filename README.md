# ceph
ansible deploy for redhat ceph on centos7

thing to consider:
- set correct info in staging/inventory or production/inventory file and use that for inventory of hosts
- for test: add the ip of your KVM bridge (e.a. virbr0 192.168.122.1) to /etc/resolv.conf for dns resolution of spinned VM's
- setup ssh (might use 'ansible -i ./inventory all -m setup' for that)
- use the playbook to setup nodes as needed

