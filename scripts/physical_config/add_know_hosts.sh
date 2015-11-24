#!/bin/bash
for i in `seq 1 70`;do
 result=$(ssh-keyscan -t rsa 10.1.0.$i 2>&1 >> ~/.ssh/tmp_hosts)
 echo $i
 if [ "$result" == ""  ]
 then
    echo $i >> unmounted_later
 fi
 done
for i in `seq 1 70`;do
 result=$(ssh-keyscan -t rsa node-$i 2>&1 >> ~/.ssh/tmp_hosts)
 echo $i
 if [ "$result" == ""  ]
 then
    echo $i >> unmounted_later
 fi
 done

for i in `seq 1 70`;do
 result=$(ssh-keyscan -t rsa 192.168.254.$i 2>&1 >> ~/.ssh/tmp_hosts)
 echo $i
 if [ "$result" == ""  ]
 then
    echo $i >> unmounted_later
 fi
 done
for i in `seq 1 70`;do
 result=$(ssh-keyscan -t rsa hdfs-$i 2>&1 >> ~/.ssh/tmp_hosts)
 echo $i
 if [ "$result" == ""  ]
 then
    echo $i >> unmounted_later
 fi


done
mv ~/.ssh/tmp_hosts  ~/.ssh/known_hosts
#rm ~/.ssh/tmp_hosts
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

