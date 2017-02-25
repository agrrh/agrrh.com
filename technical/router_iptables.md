Title: Setting up a home router
Date: 2015-07-18 13:50
Tags: iptables, router

In this article I gonna represent my home router config which also acting as a web/media/storage server and so on.

**Warning** I assume you got direct access to the host console, otherwise don't apply `DROP` policy until double-check the `ACCEPT` rules.

Here we do state that `eth0` is connected to outer world and `eth1` is our private network:

    IF_INET=eth0
    IF_PAN=eth1

Also define private network range:

    NET_PAN=10.0.0.0/24

For fresh linux installation there should be no any rules, but let's clear them just in case:

    iptables -F
    iptables -t nat -F POSTROUTING

Now let's accept local traffic and ICMP packets to don't lose the host connection:

    iptables -A INPUT -i lo -j ACCEPT
    iptables -A INPUT -i $IF_INET -p icmp --icmp-type 8 -j ACCEPT
    iptables -A INPUT -i $IF_PAN -j ACCEPT

Also we would like to save already initiated connections:

    iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT

Now define NAT rules (and make sure that `sysctl net.ipv4.ip_forward` returns `1`):

    iptables -A POSTROUTING -t nat -j MASQUERADE
    iptables -A FORWARD -i $IF_INET -o $IF_PAN -s $NET_PAN -j ACCEPT
    iptables -A INPUT -i $IF_PAN -p icmp --icmp-type 8 -j ACCEPT

Then list all the services we would like to be reachable from outside:

    # SSH (it's a good idea to change SSH port, by the way)
    iptables -A INPUT -p tcp -i $IF_INET --dport 22 -j ACCEPT

    # HTTP / HTTPS
    iptables -A INPUT -i $IF_INET -p tcp --dport 80 -j ACCEPT
    iptables -A INPUT -i $IF_INET -p tcp --dport 443 -j ACCEPT

    # SMTP
    iptables -A INPUT -i $IF_INET -p tcp --dport 25 -j ACCEPT

    # IGMP / IPTV
    iptables -A FORWARD -p igmp -i $IF_INET -o $IF_PAN -j ACCEPT
    iptables -A FORWARD -s 224.0.0.0/4 -j ACCEPT
    iptables -A INPUT -s 224.0.0.0/4 -j ACCEPT

And the last step is to close the doors and deny all what is not allowed:

    iptables -P INPUT DROP

Then I'd propose to install `iptables-persistent` and don't care about rules save and restore upon host reboot.
