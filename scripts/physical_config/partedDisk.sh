#!/bin/bash
echo "create partition sdb..."
sudo sh -c 'I | parted /dev/sdb mkpart primary ext4 445M 3000G'
if [ $? -ne 0 ]
then 
    echo "$1 failed create sdb" >> result
fi
echo "validate partition sdb..."
echo "create partition sdc..."
sudo sh -c 'I | parted /dev/sdc mkpart primary ext4 445M 3000G'
if [ $? -ne 0 ]
then 
    echo "$1 failed create sdc" >> result
fi
echo "create partition sdd..."
sudo sh -c 'I | parted /dev/sdd mkpart primary ext4 445M 3000G'
if [ $? -ne 0 ]
then 
    echo "$1 failed create sdd" >> result
fi

