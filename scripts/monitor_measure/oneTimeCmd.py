from fabric import tasks,state
from fabric.api import *
import sys
#filename="/hdfs/data1/test/hadoop_src/etc/hadoop/slaves"
#filename="/home/shenh10/docker_pack/unsuccess"
#env.hosts=[line for line in open(filename)]
env.hosts=['10.1.0.%s'%(id) for id in range(1,71)]
env.sudo_user='shenh10'
#env.hosts=['10.1.0.50']
print env.host
def file_send(localpath,remotepath):
    put(localpath,remotepath,use_sudo=True)

commands=[]
#commands.append('sudo /bin/sh /home/shenh10/scripts/scripts/physical_config/partedDisk.sh')
#commands.append('sudo /bin/sh /home/shenh10/scripts/scripts/physical_config/mountDisk.sh')
#commands.append('sudo chown -R hadoop:Student /hdfs ')
#commands.append('sudo chmod -R 777 /hdfs ')
commands.append('sudo cp /home/shenh10/scripts/scripts/physical_config/rc.local /etc/rc.local')
#commands.append('sudo /bin/sh /home/shenh10/scripts/scripts/openstack/bash/openstack_ovs_config.sh')
#commands.append('sudo timedatectl set-timezone America/Los_Angeles')
#commands.append('date')
#commands.append('mkdir -p /home/shenh10/system_monitor/results')
# No need to decorate this function with @task
#commands.append('sudo apt-get -y install sysstat')
#commands.append('sudo apt-get -y install ifstat')
#commands.append('ps aux | grep collect | grep -v grep')
#commands.append('sudo cp /home/shenh10/system_monitor/dhcp_agent.ini /etc/neutron/dhcp_agent.ini')
#commands.append('sudo grep iiis.co /etc/neutron/dhcp_agent.ini')
#commands.append("sudo docker load -i /home/shenh10/docker_pack/hadoop_final")
#commands.append("sudo sh /home/shenh10/docker_pack/install_docker.sh")
#commands.append("sudo service docker start")
#commands.append(" ps aux | grep docker | grep -v grep")
#commands.append("sh /home/shenh10/docker_pack/removeContainer.sh")
#commands.append("sudo yum -y remove docker-io")
#commands.append("sudo cp /home/shenh10/docker_pack/epel.repo /etc/yum.repos.d/")
#commands.append("sudo /bin/sh /home/shenh10/docker_pack/install_docker.sh")
#commands.append('sudo sh /home/shenh10/ovs_config.sh')
#commands.append('sudo /sbin/service neutron-openvswitch-agent restart')
#commands.append('sudo sh /home/shenh10/docker_pack/changeVolumn.sh')
#filepath='/etc/neutron/dhcp_agent.ini'
@parallel
def worker():
	for command in commands:
	#file_send(filepath,filepath)
		result=	run(command)
def main():
    print state.output
    tasks.execute(worker)

if __name__ == '__main__':
    main()
