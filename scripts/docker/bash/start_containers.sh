#!/bin/bash
id_one=$1
id_two=$2
number=$3
for i in `seq 2 $number`;do
echo "Start container with ip: 172.16."$id_one"."$id_two
core0=$(( $i*4 + 0))
core1=$(( $i*4 + 1))
core2=$(( $i*4 + 2))
core3=$(( $i*4 + 3))
echo "Allocate core:"${core0}","${core1}","${core2}","${core3}
C1=$(sudo docker run -d --net="none" -h hadoop${id_one}n${id_two}mm --name hadoop${id_one}n${id_two}mm  -t -i --cpuset=$core0,$core1,$core2,$core3 -m 16g  hadoop:final2 /bin/bash)
if [ $? -ne 0 ];then
   echo "start docker failed"
   exit 1
fi
sudo docker exec -d $C1 service ssh start
if [ $? -ne 0 ];then
   echo "start ssh service failed"
   exit 1
fi
echo "Binding veth ip"
sudo /bin/sh /home/shenh10/docker_pack/pipe.sh br-int $C1 172.16.$id_one.$id_two/16 172.16.255.255 172.16.0.1 2500

echo $id_one.$id_two
if [ $id_two -ge 254 ];then
     id_two=1
     id_one=$(( $id_one + 1 ))   
else
     id_two=$(( $id_two + 1 ))
fi
echo $id_one.$id_two
done

#echo "Setting netns..."
#netns=$(ip netns list)
#for ns in $netns;do
#   echo "Set MTU in net ns :..."$ns
#   ip netns exec $ns ifconfig eth0 mtu 1454
#   if [ $? -ne 0 ];then
#     echo "set mtu failed"
#     exit 1
#   fi
#done
#vethl=$(ifconfig | grep veth | cut -d' ' -f1)
#if [ $? -ne 0 ];then
#     echo "get vethl failed"
#     exit 1
#   fi
#for veth in $vethl;do
#    ifconfig $veth mtu 1454
#   if [ $? -ne 0 ];then
#     echo "set mtu failed"
#     exit 1
#   fi
#done
#C2=$(docker run -d -n=false -t -i hadoop:newSingleNode /bin/bash)




