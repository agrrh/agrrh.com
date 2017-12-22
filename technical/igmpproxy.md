Title: How to proxy IGMP / IPTV over NAT
Date: 2015-07-17 12:45
Tags: igmp, iptv, iptables, debian

**Outdated!** Nowadays I use [udpxy](http://www.udpxy.com/index-en.html), which is much more efficient for in-home usage.

Here's my network interfaces:

- eth0 - WAN
- eth1 - LAN

Iptables default policy is DROP, so we need to allow IGMP traffic:

```
iptables -A FORWARD -p igmp -i eth0 -o eth1 -j ACCEPT

iptables -A FORWARD -s 224.0.0.0/4 -j ACCEPT
iptables -A INPUT -s 224.0.0.0/4 -j ACCEPT
```

Then we need to build [igmpproxy](http://sourceforge.net/projects/igmpproxy/), взять его можно здесь:

```
cd /usr/src
# wget the source file
cd igmpproxy-*
checkinstall -D -y --pkgname=igmpproxy
dpkg -i igmpproxy_0.1-beta2-1_amd64.deb
```

Customize config in `/etc/igmpproxy.conf`, you could get default one from `/usr/local/etc/igmpproxy.conf`, but there's also my own example:

```
# keep turned off while more than 1 client
#quickleave

# input interface
phyint eth0 upstream  ratelimit 0  threshold 1

# multicast default addresses
altnet 224.0.0.0/4

# PANs just to be sure
altnet 192.168.0.0/16
altnet 172.16.0.0/12
altnet 10.0.0.0/8

# ISP-specific addresses
altnet 93.100.0.0/16

# output interface
phyint eth1 downstream  ratelimit 0  threshold 1

# wireless is ignored
phyint mon.wlan0 disabled
phyint wlan0 disabled
```

Now we are ready to go:

```
igmpproxy -d /etc/igmpproxy.conf > /var/log/igmpproxy.log 2>&1 &
```

Yes, in this particular situatuin I just placed it somewhere like `/etc/rc.local`, but to keep things organized you would like to create [systemd service](https://www.devdungeon.com/content/creating-systemd-service-files).
