Title: How to proxy IGMP / IPTV over NAT
Date: 2015-07-17 12:45
Tags: igmp, iptv, iptables

*This article is kinda old!* I'm currently using [udpxy](http://www.udpxy.com/index-en.html) which probably much better solution for PAN usage.

First, here's my gateway scheme:

- eth0 - WAN
- eth1 - LAN

My iptables default INPUT policy was DROP, so I needed to allow IGMP traffic:

    iptables -A FORWARD -p igmp -i eth0 -o eth1 -j ACCEPT

    iptables -A FORWARD -s 224.0.0.0/4 -j ACCEPT
    iptables -A INPUT -s 224.0.0.0/4 -j ACCEPT

Now get igmpproxy:
http://sourceforge.net/projects/igmpproxy/

    cd /usr/src
    # wget the source file
    cd igmpproxy-*
    checkinstall -D -y --pkgname=igmpproxy
    dpkg -i igmpproxy_0.1-beta2-1_amd64.deb

Afterwards yo will need to start it and customize the config:

    cp /usr/local/etc/igmpproxy.conf /etc/igmpproxy.conf

Here's my config for example:

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

    # ISP-specific addresses
    altnet 93.100.0.0/16

    # Output interface
    phyint eth1 downstream  ratelimit 0  threshold 1

    # Wireless is ignored
    phyint mon.wlan0 disabled
    phyint wlan0 disabled

An you could then start it with following command:

    igmpproxy -d /etc/igmpproxy.conf > /var/log/igmpproxy.log 2>&1 &

Of course, better idea is to use init-scripts, but in Debian-family distros default init systems changing too fast right now, so you could try it on your own :)
