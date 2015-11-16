#!/bin/sh
passwd ubuntu<<EOF
ubuntu
ubuntu
EOF
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
service ssh restart
eth0_ip=$(/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}')
id1=$(/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | cut -d' ' -f1 | cut -d. -f3)
id2=$(/sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | cut -d' ' -f1 | cut -d. -f4)
id=$id1'n'$id2
sudo cat > /etc/hostname <<EOD
hadoop$id
EOD
hostname hadoop$id
hostname
sudo cat >> /etc/hosts << END
$eth0_ip hadoop$id
END
sudo cat > /etc/network/interfaces.d/eth1.cfg << EOF

auto eth1

iface eth1 inet dhcp

EOF

sudo ifup eth1
