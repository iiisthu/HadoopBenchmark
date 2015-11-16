#!/bin/bash
echo "mkfs sdb"
sudo sh -c 'yes y | /sbin/mkfs -t ext4 /dev/sdb'
if [ $? -ne 0 ]
then
    echo "$1 failed formatting sdb" >> result
fi

echo "mkfs sdc"
sudo sh -c 'yes y | /sbin/mkfs -t ext4 /dev/sdc'
if [ $? -ne 0 ]
then
    echo "$1 failed formatting sdc" >> result
fi
echo "mkfs sdd"
sudo sh -c 'yes y | /sbin/mkfs -t ext4 /dev/sdd'
if [ $? -ne 0 ]
then
    echo "$1 failed formatting sdd" >> result
fi

echo "create /data1/test"
sudo mkdir -p /hdfs/data1/test
if [ $? -ne 0 ]
then
    echo "$1 failed create folder" >> result
fi
echo "create /data2"
sudo mkdir -p /hdfs/data2
if [ $? -ne 0 ]
then
    echo "$1 failed create folder" >> result
fi
echo "create /data3"
sudo mkdir -p /hdfs/data3
if [ $? -ne 0 ]
then
    echo "$1 failed create folder" >> result
fi

echo "chown"
sudo chown -R hadoop:Student /hdfs
echo "chmod"
sudo chmod -R 777 /hdfs
echo " modify fstab if not configured"
result=$(sudo cat /etc/fstab | grep sdc)
 if [ "$result" == ""  ]
 then
sudo sh -c 'cat /home/shenh10/hadoop/fstab_input >> /etc/fstab'
if [ $? -ne 0 ]
then
    echo "$1 failed changing fstab"
fi
fi
echo "mount all disk in /etc/fstab"
sudo mount -a
if [ $? -ne 0 ]
then
    echo "$1 failed mount all"
fi

