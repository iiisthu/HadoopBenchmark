#!/bin/bash
filename="/hdfs/data1/test/hadoop_src/etc/hadoop/slaves"
count=1
id=1
for ip in `cat $filename`;do
#ip='10.6.0.50'
    if [ $count -le 62 ];then
    actuall_id=$(( $id *4 ))
    echo $actuall_id
    ssh $ip "sudo sh /home/shenh10/docker_pack/start_containers.sh 20 $actuall_id 4 " 
    else
	if [ $count = 63 ];then
	    id=1
	fi
    actuall_id=$(( $id *4 ))
    echo $actuall_id
    ssh $ip "sudo sh /home/shenh10/docker_pack/start_containers.sh 21 $actuall_id 4 " 
    fi
   # echo 'count: '$count
   # echo 'id :'$id
    count=$(($count+1))
    id=$(($id+1))
done
