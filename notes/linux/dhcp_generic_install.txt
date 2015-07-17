# How to install generic dhcp server

apt-get update

apt-get install isc-dhcp-server

nano /etc/dhcp/dhcpd.conf

----------------------%<----------------------

# default nameservers
option domain-name-servers 192.168.0.1, 8.8.8.8;

# declare subnet and allowed hosts range
subnet 192.168.0.0 netmask 255.255.255.0 {
  range 192.168.0.2 192.168.0.254;
  option routers 192.168.0.1;
}

# static lease example
host myworkstation {
  hardware ethernet aa:bb:cc:dd:ee:ff;
  fixed-address 192.168.1.123;
}

----------------------%<----------------------

/etc/init.d/isc-dhcp-server restart