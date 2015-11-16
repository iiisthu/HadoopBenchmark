#!/bin/bash
for i in `seq 1 2`;do
nova boot --flavor 6 --key-name mykey2 --image 43d23917-a813-45bc-8012-5eb567d0b9e0  --security-groups default --nic net-id=776c587e-1e9a-4020-adbc-0519693b4763 --nic net-id=c9b0740e-906e-49ea-94b8-3962807cb874 --user-data boot-scripts.sh  hanshen_vm
sleep 30
done
