#/bin/bash

devs=$(ls /dev/mapper/docker-*-*  | grep -v pool | grep -v base | cut -d'/' -f4)
for device in $devs;do
    DEV=$device
    echo $DEV
    sudo dmsetup table $DEV | sed "s/0 [0-9]* thin/0 $((100*1024*1024*1024/512)) thin/" | sudo dmsetup load $DEV
    sudo dmsetup resume $DEV
    sudo resize2fs /dev/mapper/$DEV
    containers=$(sudo docker ps -a | grep hadoop | cut -d' ' -f1)
    for container in $containers;do
    sudo docker start $container
    done
done
