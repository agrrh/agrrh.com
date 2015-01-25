How to proxy IGMP / IPTV over NAT

First, here's my gateway scheme:

eth0 - WAN
eth1 - LAN

! iptables default INPUT policy was DROP, so I needed to allow IGMP traffic:

```
iptables -A FORWARD -p igmp -i eth0 -o eth1 -j ACCEPT

iptables -A FORWARD -s 224.0.0.0/4 -j ACCEPT
iptables -A INPUT -s 224.0.0.0/4 -j ACCEPT
```

First, get igmpproxy:
http://sourceforge.net/projects/igmpproxy/

```
cd /usr/src
# wget
cd igmpproxy-*
checkinstall -D -y --pkgname=igmpproxy
dpkg -i igmpproxy_0.1-beta2-1_amd64.deb
```
Afterwards yo will need to start it and 

```
cp /usr/local/etc/igmpproxy.conf /etc/igmpproxy.conf
```

```
# cat /etc/igmpproxy.conf

# Not sure what's this :)
#quickleave

# Input interface
phyint eth0 upstream  ratelimit 0  threshold 1

# multicast default addresses
altnet 224.0.0.0/4

# PANs just to be sure
altnet 192.168.0.0/16
altnet 172.16.0.0/12
altnet 10.0.0.0/8

# Provider-specific addresses
altnet 93.100.0.0/16

# Output interface
phyint eth1 downstream  ratelimit 0  threshold 1

# Wireless is ignored
phyint mon.wlan0 disabled
phyint wlan0 disabled
```

And let's start it!

```
igmpproxy -d /etc/igmpproxy.conf > /var/log/igmpproxy.log 2>&1 &
```
