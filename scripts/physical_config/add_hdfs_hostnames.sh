#!/bin/bash
for i in `seq 1 70`;do
 result=$(echo "192.168.254.$i  hdfs-$i hdfs-$i.domain.tld" 2>&1 >> etc_hosts)
 echo $i
 if [ "$result" == ""  ]
 then
    echo $i >> failed_add_to_host
 fi
 done
#sudo cat etc_hosts >> /etc/hosts
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

