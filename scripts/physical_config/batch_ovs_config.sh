#!/bin/bash
echo "Start batch create virtual ports..."
#for i in `seq 50 50`;do
# echo $i
# result=$(ssh -o StrictHostKeyChecking=no -t shenh10@10.1.0.$i "sudo  /home/shenh10/scripts/scripts/openstack/bash/openstack_ovs_config.sh" )
#done
#echo "Start batch check connection..."
for i in `seq 1 70`;do
  result=$(ping -c 1 "192.168.254.$i")   
echo $i
 if [ "$result" == ""  ]
 then
    echo $i >> unsuccess_vps
 fi

done
echo "Done..."
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

