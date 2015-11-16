#!/bin/bash
#yes | mkfs /dev/sdb
#yes | mkfs /dev/sdc
#yes | mkfs /dev/sdd
df -h
/sbin/fdisk -l /dev/sdb
/sbin/fdisk -l /dev/sdc
/sbin/fdisk -l /dev/sdd
