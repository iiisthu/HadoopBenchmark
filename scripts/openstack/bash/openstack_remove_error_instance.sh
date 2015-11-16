#!/bin/bash
result=$(nova list |grep ERROR | cut -d' ' -f2)
#result=$(nova list |grep powering | cut -d' ' -f2)
for i in $result;do
echo $i
nova delete $i
done
