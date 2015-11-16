#!/bin/bash

nodes=$(nova-manage vm list | grep shenh10 | cut -d$' ' -f2 )
echo ""> count_result
count=0
for i in `seq 1 9`;do
  number=$(echo $nodes | sed 's/ /\n/g' | grep n00$i | wc -l)
  echo $i'    '$number >>count_result
  count=$(( $count + $number ))
done
for i in `seq 10 55`;do
  number=$(echo $nodes | sed 's/ /\n/g' | grep n0$i | wc -l)
  echo $i'    '$number >>count_result
  if [ $i -le 56 ];then 
  count=$(( $count + $number ))
  fi
done
#for i in `seq 87 99`;do
#  number=$(echo $nodes | sed 's/ /\n/g' | grep n0$i | wc -l)
#  echo $i'    '$number >>count_result
#done
#for i in `seq 100 125`;do
#  number=$(echo $nodes | sed 's/ /\n/g' | grep n$i | wc -l)
#  echo $i'    '$number >>count_result
#done
echo $count
