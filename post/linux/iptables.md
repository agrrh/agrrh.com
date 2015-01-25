# iptables usage

# block ip
iptables -A INPUT -s 1.2.3.4 -j DROP

# block ip with specific protocol
iptables -A OUTPUT -p tcp -d 1.2.3.4 -j DROP
iptables -A OUTPUT -p udp -d 1.2.3.4 -j DROP

# block port
iptables -A INPUT -p tcp --dport 22 -j DROP

# block subnet
iptables -A INPUT -s 12.34.56.0/24 -j DROP

# block part of subnet with iprange module
iptables -I INPUT -m iprange --src-range 192.168.1.10-192.168.1.13 -j DROP

# block full net except 1 host
iptables -I INPUT ! -s 1.2.3.4 -j DROP

# block SMTP for each host except trusted one
iptables -I INPUT -p tcp --dport 25 ! -s 1.2.3.4 -j DROP

# same as
iptables -I INPUT -p tcp --dport 25 -j DROP
iptables -I INPUT -p tcp --dport 25 -s 1.2.3.4 -j ACCEPT

# default policy
iptables -P INPUT DROP

# redirect port to another port
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080

# redirect port to another IP
# sysctl net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -j MASQUERADE
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.0.2:8080

# rate limit 3/60s
iptables -I INPUT -p tcp --dport 22 -m state --state NEW -m recent --set
iptables -I INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 3 -j DROP

# block by user
iptables -A OUTPUT -m owner --uid-owner USER -j DROP

# block countries
iptables -I INPUT -m geoip ! --src-cc RU,UA -j DROP
iptables -I OUTPUT -m geoip ! --dst-cc RU,UA -j DROP
