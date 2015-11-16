#!/bin/bash
set -e

BRIDGE=$1
GUESTNAME=$2
IPADDR=$3
BROADCAST=$4
GWADDR=$5
VLANTAG=$6

[ "$IPADDR" ] || {
    echo "Syntax:"
    echo "p/sbin/ipework <hostinterface> <guest> </sbin/ipaddr>/<subnet> <broadcast> <gateway> [vlan tag]"
    exit 1
}

# Step 1: Find the guest (for now, we only support LXC containers)
while read dev mnt fstype options dump fsck
do
    [ "$fstype" != "cgroup" ] && continue
    echo $options | grep -qw devices || continue
    CGROUPMNT=$mnt
done < /proc/mounts

[ "$CGROUPMNT" ] || {
    echo "Could not locate cgroup mount point."
    exit 1
}

N=$(find "$CGROUPMNT" -name "$GUESTNAME*" | wc -l)
case "$N" in
    0)
	echo "Could not find any container matching $GUESTNAME."
	exit 1
	;;
    1)
	true
	;;
    *)
	echo "Found more than one container matching $GUESTNAME."
	exit 1
	;;
esac

NSPID=$(head -n 1 $(find "$CGROUPMNT" -name "$GUESTNAME*" | head -n 1)/tasks)
[ "$NSPID" ] || {
    echo "Could not find a process inside container $GUESTNAME."
    exit 1
}

# Step 2: Prepare the working directory
mkdir -p /var/run/netns
rm -f /var/run/netns/$NSPID
ln -s /proc/$NSPID/ns/net /var/run/netns/$NSPID

# Step 3: Creating virtual interfaces
LOCAL_IFNAME=vethl$NSPID
GUEST_IFNAME=vethg$NSPID
/sbin/ip link add name $LOCAL_IFNAME type veth peer name $GUEST_IFNAME
/sbin/ip link set $LOCAL_IFNAME up

# Step 4: Adding the virtual interface to the bridge
/sbin/ip link set $GUEST_IFNAME netns $NSPID
if [ "$VLANTAG" ]
then
	/usr/bin/ovs-vsctl add-port $BRIDGE $LOCAL_IFNAME tag=$VLANTAG
else
	/usr/bin/ovs-vsctl add-port $BRIDGE $LOCAL_IFNAME
fi

# Step 5: Configure netwroking within the container
/sbin/ip netns exec $NSPID /sbin/ip link set $GUEST_IFNAME name eth0
/sbin/ip netns exec $NSPID /sbin/ip addr add $IPADDR broadcast $BROADCAST dev eth0
/sbin/ip netns exec $NSPID /sbin/ip addr add 127.0.0.1 dev lo
/sbin/ip netns exec $NSPID /sbin/ip link set eth0 up
/sbin/ip netns exec $NSPID /sbin/ip link set lo up
/sbin/ip netns exec $NSPID /sbin/ip route add default via $GWADDR 
