#/bin/bash
filename='/hdfs/data1/test/hadoop_src/etc/hadoop/slaves'
for i in `cat $filename`;do
    echo $i
    ssh $i 'sudo /sbin/service docker restart'
    #ssh $i 'sudo docker load -i /home/shenh10/docker_pack/hadoop_final'

done
