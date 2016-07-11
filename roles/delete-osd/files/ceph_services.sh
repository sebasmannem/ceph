#!/bin/bash
systemctl | grep -Eo 'ceph-osd@[0-9]+'
