#!/bin/bash

# save to /etc/network/if-pre-up.d/router

SSH_PORT=22

# Flush actual rules
iptables -F
iptables -t nat -F POSTROUTING

# Set default policies

# Deny all what is not allowed
iptables -P INPUT DROP
#iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# Accept local traffic and ICMP packets
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -i eth0 -p icmp --icmp-type 8 -j ACCEPT

# Accept already initiated connections
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT

# Accept all traffic from LAN
iptables -A INPUT -i eth1 -j ACCEPT

# NAT
iptables -A POSTROUTING -t nat -j MASQUERADE
# Make sure net.ipv4.ip_forward is set to 1
iptables -A FORWARD -i eth0 -o eth1 -s 192.168.51.0/24 -j ACCEPT
iptables -A INPUT -i eth1 -p icmp --icmp-type 8 -j ACCEPT

# Services

# SSH
iptables -A INPUT -p tcp -i eth0 --dport $SSH_PORT -j ACCEPT

# HTTP / HTTPS
iptables -A INPUT -i eth0 -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -i eth0 -p tcp --dport 443 -j ACCEPT

# Transmission web interface
iptables -A INPUT -i eth0 -p tcp --dport 9091 -j ACCEPT

# SMTP
iptables -A INPUT -i eth0 -p tcp --dport 25 -j ACCEPT

# btsync
# replaced with nginx
# iptables -A INPUT -p tcp -m tcp --dport 8888 -j ACCEPT

# IPTV
iptables -A FORWARD -p igmp -i eth0 -o eth1 -j ACCEPT
iptables -A FORWARD -s 224.0.0.0/4 -j ACCEPT
iptables -A INPUT -s 224.0.0.0/4 -j ACCEPT

igmpproxy -d /etc/igmpproxy.conf > /var/log/igmpproxy.log 2>&1 &
