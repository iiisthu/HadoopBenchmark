#!/bin/bash
#nova-manage vm list | grep shenh10 | column -t | cut -d' ' -f3 | egrep -o '[[:digit:]]{3}' | bc > arised_nodes
#filename="arised_nodes"
filename='/hdfs/data1/test/hadoop_src/etc/hadoop/slaves'
for src in `cat $filename`;do
    for dst in `cat $filename`;do
	echo "From $src to $dst:"
	echo "From $src to $dst:" >> /home/shenh10/iperfRes.txt
	ssh $src "iperf -c $dst  | grep sec | column -t |cut -d' ' -f13,15 >> /home/shenh10/iperfRes.txt"
    done
done
