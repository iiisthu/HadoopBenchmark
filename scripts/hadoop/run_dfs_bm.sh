#!/bin/bash
#for i in `seq 8 17`;do
#export RD_NUM_OF_FILES=$(( 2 ** $i ))
#export RD_FILE_SIZE=512
#export WT_NUM_OF_FILES=$(( 2 ** $i ))
#export WT_FILE_SIZE=512 
#
filename="test"
testbench='wordcount'
for i in `cat $filename`;do
scale=$i
echo $scale
echo  "hibench.scale.profile  	      	       $scale " > workloads/$testbench/conf/10-$testbench-userdefine.conf 
for i in `seq 1 10`;do
	if [ $i = 1 ];then
		export PREPARE=1
	fi
#echo "start dfsio $scale round $i...."$(date) >> run_log
bin/run-all.sh
mv report/$testbench/mapreduce report/$testbench/mapreduce-$scale-round$i
#mv report/dfsioe/mapreduce-write report/dfsioe/mapreduce-write-$scale-round$i
#echo "Finish dfsio $scale....round $i"$(date) >> run_log
export PREPARE=0
done
done
##for i in `seq 2 2`;do
#mapram=$(bc <<< " $i*2*1024")
#mapjvm=$(bc <<< "$mapram * 4 / 5 ")
#redram=$(bc <<< "($i+2)*2*1024 ")
#redjvm=$(bc <<< "$redram* 4 / 5 ")
#echo "Map RAM: "$mapram";Reduce RAM:"$redram";Map JVM size:"$mapjvm";Reduce JVM:"$redjvm
##sed -i "s/MAPRAM/${mapram}/g" ~/hadoop/etc/hadoop/mapred-site.xml
#sed -i "s/REDRAM/${redram}/g" ~/hadoop/etc/hadoop/mapred-site.xml
#sed -i "s/REDJVM/${redjvm}/g" ~/hadoop/etc/hadoop/mapred-site.xml
#sed -i "s/MAPJVM/${mapjvm}/g" ~/hadoop/etc/hadoop/mapred-site.xml
#sed -i "s/$mapram/MAPRAM/g" ~/hadoop/etc/hadoop/mapred-site.xml
#sed -i "s/$redram/REDRAM/g" ~/hadoop/etc/hadoop/mapred-site.xml
#sed -i "s/$redjvm/REDJVM/g" ~/hadoop/etc/hadoop/mapred-site.xml
#sed -i "s/$mapjvm/MAPJVM/g" ~/hadoop/etc/hadoop/mapred-site.xml
#done
##mv report/dfsioe/mapreduce-read report/dfsioe/mapreduce-read-${scale}1
#mv report/dfsioe/mapreduce-write report/dfsioe/mapreduce-write-${scale}1
