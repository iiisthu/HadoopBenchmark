#!/bin/bash

#filename="unused"
#for i in `cat $filename`;do
#  echo $i
#  done
#
#for i in `seq 76 86`;do
#echo $i
#  image=$(nova hypervisor-servers n0$i | grep instance |cut -d' ' -f2)
#  search=$(nova list  --all-tenants | grep shenh10 | grep $image)
#    #echo "Result:"$search"."
#    if [ "$search" == "" ];then
#      echo " "
#    else
#      echo "Delete "$image" on node"$i
#      nova delete $image
#    fi
#done
count=0
deleteNum=3
nodes=$(nova-manage vm list | grep shenh10 | cut -d$' ' -f2 )
for i in `seq 2 55`;do
	if [ $i -le 9 ]; then
		name=n00$i
		number=$(echo $nodes | sed 's/ /\n/g' | grep $name | wc -l)
	elif [ $i -ge 100 ]; then
		name=n$i
		number=$(echo $nodes | sed 's/ /\n/g' | grep $name | wc -l)
	else
		name=n0$i
		number=$(echo $nodes | sed 's/ /\n/g' | grep $name | wc -l)
	fi
	if [ $number -ge 6  ]
	then
		echo "On node$i $number instances..."
		images=$(nova hypervisor-servers $name | grep instance | cut -d' ' -f2)
		count_internal=0
		for image in $images;do
			search=$(nova list  --all-tenants | grep shenh10 | grep $image)
			echo "Result:"$search"."
			if [ "$search" == "" ];then
				echo " "
			else
				if [ $count -ge $deleteNum ];
				then
					break
				fi
				echo "Delete "$image" on node"$i
				nova delete $image
				count_internal=$(( $count_internal+1 ))
				count=$(( $count+1 ))
			fi
			if [ $count_internal -ge 1 ];
			then
				break
			fi
		done
	fi
	if [ $count -ge $deleteNum ];
	then
		break
	fi
done

