#!/bin/bash
cp ovs_neutron_agent.py  /usr/lib/python2.6/site-packages/neutron/plugins/openvswitch/agent/ovs_neutron_agent.py
/sbin/service neutron-openvswitch-agent restart
id=$(hostname -I | cut -d' ' -f1 | awk -F '.' '{print $4}')
add_ip="172.16.0."$id


#echo "set ip address of vp0 ...$add_ip"
#ovs-vsctl add-port br-int vp0 tag=2500 -- set Interface vp0 type=internal
#/sbin/ip addr add $add_ip/16 dev vp0
/sbin/ifconfig vp0 ${add_ip}/16
/sbin/ifconfig vp0 up
##ifconfig vp0 mtu 1454
