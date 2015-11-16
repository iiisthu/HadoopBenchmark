#!/bin/bash
veths=$(sudo ovs-vsctl show | grep veth | grep Port | cut -d'"' -f2)

for veth in $veths;do
   echo "Delete"$veth
   sudo  ovs-vsctl del-port $veth
   sudo /sbin/ip link delete $veth
   id=$(echo $veth | sed 's/vethl//g' )
  sudo /sbin/ip netns delete $id
done
containers=$(sudo docker ps -a | grep hadoop | cut -d' ' -f1)
for container in $containers;do
    sudo docker rm  -f $container
    if [ $? -ne 0 ];then
      echo "remove container $container failed"
      exit 1
    fi
    sleep 10
done


