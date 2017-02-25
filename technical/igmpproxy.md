Title: How to proxy IGMP / IPTV over NAT
Date: 2015-07-17 12:45
Tags: igmp, iptv, iptables, debian

*Это старая статья!* Я давно использую [udpxy](http://www.udpxy.com/index-en.html), который намного более удобен для домашнего использования.

Вот моя схема подключения интерфейсов на роутере:

- eth0 - WAN
- eth1 - LAN

В iptables политка по умолчаню для INPUT, конечно, DROP, так что надо разрешить IGMP-трафик:

```bash
iptables -A FORWARD -p igmp -i eth0 -o eth1 -j ACCEPT

iptables -A FORWARD -s 224.0.0.0/4 -j ACCEPT
iptables -A INPUT -s 224.0.0.0/4 -j ACCEPT
```

Далее собираем igmpproxy, взять его можно здесь: http://sourceforge.net/projects/igmpproxy/

```bash
cd /usr/src
# wget the source file
cd igmpproxy-*
checkinstall -D -y --pkgname=igmpproxy
dpkg -i igmpproxy_0.1-beta2-1_amd64.deb
```

Далее кастомизируем себе конфиг:

```bash
cp /usr/local/etc/igmpproxy.conf /etc/igmpproxy.conf
```

Here's my config for example:

```bash
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

А далее можно запускать:

```bash
igmpproxy -d /etc/igmpproxy.conf > /var/log/igmpproxy.log 2>&1 &
```

Да-да, в том конкретном случае я просто запихал это куда-то в `/etc/rc.local`, вообще не думая про то, как правильно.

Правильно было бы написать конкретный init-скрипт и включить его в собранный ранее пакет.
