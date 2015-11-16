#/bin/bash
echo "stop docker service ..."
sudo service docker stop
if [ $? -ne 0 ];then
    echo "Docker stop failure"
    exit 1
fi

echo "rm docker dir ..."
sudo rm -rf /var/lib/docker
if [ $? -ne 0 ];then
    echo "remove dir failed!"
    exit 1
fi
echo "mkdir devicemapper dir ..."
sudo mkdir -p /var/lib/docker/devicemapper/devicemapper
if [ $? -ne 0 ];then
    echo "mkdir failed!"
    exit 1
fi

echo "set volumn to docker ..."
sudo dd if=/dev/zero of=/var/lib/docker/devicemapper/devicemapper/data bs=1G count=0 seek=1024

if [ $? -ne 0 ];then
    echo "dd failed!"
    exit 1
fi

echo "start docker service ..."
sudo service docker start

if [ $? -ne 0 ];then
    echo "start failed!"
    exit 1
fi

echo "check docker info ..."
sudo docker info
if [ $? -ne 0 ];then
    echo "check docker info failed!"
    exit 1
fi
echo "load docker  ..."
sudo docker load -i /home/shenh10/docker_pack/hadoop_save 
if [ $? -ne 0 ];then
    echo "load image failed"
    exit 1

fi
