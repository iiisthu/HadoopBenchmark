#!/bin/bash

sudo yum -y install docker-io
if [ $? -ne 0 ]
then
    echo "install docker-io failed" >> install_docker_result.txt
    exit 1
fi
sudo /sbin/service docker start
if [ $? -ne 0 ]
then
    echo "start docker service failed" >> install_docker_result.txt
    exit 1
fi
sudo /sbin/chkconfig docker on
if [ $? -ne 0 ]
then
    echo "make docker startup service failed" >> install_docker_result.txt
    exit 1
fi
sudo docker info 
if [ $? -ne 0 ]
then
    echo "Check docker info failed" >> install_docker_result.txt
    exit 1
fi
