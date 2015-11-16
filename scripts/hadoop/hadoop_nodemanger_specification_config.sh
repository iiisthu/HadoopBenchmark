#!/bin/bash

id=$(hostname -I | cut -d' ' -f1 | awk -F '.' '{print $4}')
add_ip="10.6.0."$id
echo $add_ip
sed -i  "s/NMADDRESS/$add_ip/g"    '/hdfs/data1/test/hadoop_src/etc/hadoop/yarn-site.xml'
