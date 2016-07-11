#!/bin/bash
OSD_FOLDER=$1
sed -i -r 's|^([^#].* '$OSD_FOLDER'/? .*)|#\1|' /etc/fstab
