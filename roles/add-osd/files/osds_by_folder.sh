#!/bin/bash
osd_folder=$1
ls -d "$osd_folder"* | sed 's|'${osd_folder}'||'
