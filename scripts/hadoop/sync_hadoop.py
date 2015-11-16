from fabric import tasks,state
from fabric.api import *
import sys
filename="/home/shenh10/system_monitor/hadoop_src/etc/hadoop/slaves"
env.hosts=[line for line in open(filename)]
#env.hosts=['10.1.0.%s'%(id) for id in range(1,125)]
#env.hosts=['10.1.0.50']
print env.host
def file_send(localpath,remotepath):
    put(localpath,remotepath,use_sudo=True)

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
#commands.append("sudo sed -i 's/dhcp_domain = iiis.co 2.iiis.co/#dhcp_domain = iiis.co 2.iiis.co/g' /etc/neutron/dhcp_agent.ini")
#filepath='/hdfs/data1/test/hadoop_src'
#commands.append('cp -r /home/shenh10/system_monitor/hadoop_src/etc/hadoop/mapred-site.xml /hdfs/data1/test/hadoop_src/etc/hadoop')
#commands.append('cp -r /home/shenh10/system_monitor/hadoop_src/etc/hadoop/hdfs-site.xml /hdfs/data1/test/hadoop_src/etc/hadoop')
commands.append('cp -r /home/shenh10/system_monitor/hadoop_src/etc/hadoop/*-site.xml /hdfs/data1/test/hadoop_src/etc/hadoop/')
commands.append('cp -r /home/shenh10/system_monitor/hadoop_src/etc/hadoop/slaves /hdfs/data1/test/hadoop_src/etc/hadoop/')
commands.append('/bin/sh /home/shenh10/system_monitor/changeDataManager.sh')
#commands.append('/bin/sh /home/shenh10/hadoop/remove_datanode_remains.sh')
@parallel
def worker():
	for command in commands:
	#file_send(filepath,'/hdfs/data1/test/')
		result=	run(command)
def main():
    print state.output
    tasks.execute(worker)

if __name__ == '__main__':
    main()
