#!/bin/bash
for i in `seq 1 70`;do
    ping -c 1 192.168.254.$i
 if [ $? -ne 0  ]
 then
    echo $i >> uncreate_later
 fi
done

