#!/bin/bash
sudo cat /etc/security/limits.conf | grep shenh10
if [ $? -ne  0 ];then
  sudo echo "shenh10          soft    nproc          65535" >> /etc/security/limits.conf 
  sudo echo "shenh10           hard    nproc          65535" >> /etc/security/limits.conf
fi
