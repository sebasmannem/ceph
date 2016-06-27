#!/bin/bash
systemctl | sed -nr '/ceph-osd@[0-9]+\.service/{s/ceph-osd@([0-9]+)\.service.*/\1/;p}'
