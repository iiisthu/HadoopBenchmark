from fabric import tasks,state
from fabric.api import *
import sys
filename="/hdfs/data1/test/hadoop_src/etc/hadoop/slaves"
env.hosts=[line for line in open(filename)]
#filename="/home/shenh10/docker_pack/unsuccess"
#env.hosts=['10.6.0.38']
#env.hosts=['10.1.0.%s'%(id) for id in range(1,125)]
#env.hosts=['10.1.0.50']
print env.host
def file_send(localpath,remotepath):
    put(localpath,remotepath,use_sudo=True)

class FabricException(Exception):
    pass

env.abort_exception = FabricException
commands=[]
#commands.append('sudo timedatectl set-timezone America/Los_Angeles')
#commands.append('date')
#commands.append('mkdir -p /home/shenh10/system_monitor/results')
# No need to decorate this function with @task
#commands.append('sudo apt-get -y install sysstat')
#commands.append('sudo apt-get -y install ifstat')
#commands.append('ps aux | grep collect | grep -v grep')
#commands.append('sudo cp /home/shenh10/system_monitor/dhcp_agent.ini /etc/neutron/dhcp_agent.ini')
#commands.append('sudo grep iiis.co /etc/neutron/dhcp_agent.ini')
commands.append("sudo service docker stop")
#commands.append("sudo docker load -i /home/shenh10/docker_pack/hadoop_final")
#commands.append("sudo sh /home/shenh10/docker_pack/install_docker.sh")
#commands.append(" ps aux | grep docker | grep -v grep")
#filepath='/etc/neutron/dhcp_agent.ini'
@parallel
def worker():
    for command in commands:
	#file_send(filepath,filepath)
	with settings(warn_only=True):
	    result= run(command)
def main():
    print state.output
    tasks.execute(worker)

if __name__ == '__main__':
    main()
