#!/bin/bash
#for i in `seq 71 125`;do
# result=$(ssh -o StrictHostKeyChecking=no  shenh10@10.1.0.$i "sudo sh" < ./checkmount.sh)
# echo $i
# if [ "$result" == ""  ]
# then
#    echo $i >> unmounted_later
# fi
#result=$(ssh -o StrictHostKeyChecking=no  shenh10@10.1.0.$i "sudo cat /etc/fstab | grep sdg")
# if [ "$result" == ""  ]
# then
#    echo $i >> unconfigedfstab_later
# fi
#
# ssh -o StrictHostKeyChecking=no  shenh10@10.1.0.$i "sudo ls -al /hdfs"
# if [ $? -ne 0  ]
# then
#    echo $i >> uncreate_later
# fi
#done
filename='/hdfs/data1/test/hadoop_src/etc/hadoop/slaves'
for i in `cat $filename`; do
  ping -c 1 $i
  if [ $? -ne 0 ]
  then
    echo $i >> unreachableNode
  fi
done
