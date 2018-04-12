Date: 2018-03-23 22:47
Category: Technical
Title: Wireguard, a kernel-space VPN
Modified: 2018-03-25 11:14
Tags: vpn, security, wireguard

[WireGuard](https://www.wireguard.com/) is a VPN toolkit. It's written in C, [faster](https://www.wireguard.com/performance/) than OpenVPN/IPsec and much [simpler](https://www.wireguard.com/quickstart/) to use.

Instead of reading number of pages of "How to generate keys" tutorial and then heading to "How to install and configure daemon" when dealing with OpenVPN, you could just set thing up in few commands. Despite this easy-to-run nature, I gonna provide you with full instructions on how to run wireguard as system service, not single-use process. This, of course, makes tutorial a little bigger. See [quickstart section](https://www.wireguard.com/quickstart/) for details on how to test wireguard once.

In all cases you'd like to install wireguard and generate pair of public/private keys to authenticate access:

```
apt install software-properties-common

# Install actual kernel headers, you need those to build DKMS modules
apt install linux-image-generic-hwe-16.04 --install-suggests

add-apt-repository ppa:wireguard/wireguard
apt install wireguard

# Reboot to apply new kernel

# Check if module loaded and load it if it's not
( lsmod | grep wireguard ) || modprobe wireguard

# Generate keys
cd /etc/wireguard
wg genkey | tee privatekey
chmod 0600 privatekey
wg pubkey < privatekey | tee publickey

# Prepare config file
touch /etc/wireguard/wg0.conf
chmod -v 0600 /etc/wireguard/wg0.conf
```

Then, there is two ways to run the VPN. One could setup interface manually and then attach IP address and routes. Much simpler way is to use `wg-quick` utility which will do it automatically.

Let's now configure hosts as 2 peer-to-peer network and server which is able to accept multiple clients.

### Peer-to-peer

Both clients should be configured identically:

```
# /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <paste private key here>
Address = 10.0.5.<set address for this host>/32
ListenPort = 51820

[Peer]
PublicKey = <paste public key here>
AllowedIPs = <paste other host's internal IP here>/32
Endpoint = <paste other host's external IP here>:51820
```

Note: This config is written to be used with `wg-quick` explicitly, make sure to remove excessive options (e.g. Address) if you would like to set things up manually via `/etc/network/interfaces` or any other way.

Then you just need to bring the things up:

```
wg-quick up wg0
ping <internal IP of ther host>
```

And enable the service if you would like to make config persistent:

```
systemctl enable wg-quick@wg0
```

### Client-Server

In this setup, server is just listens for incoming connections while clients are not going to await for anything, only trying to reach the server host.

Server configuration example:

```
# /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <paste private key here>
Address = 10.0.5.1/24
ListenPort = 51820
SaveConfig = true

# Repeat this section for each client
[Peer]
PublicKey = <paste client public key here>
AllowedIPs = 10.0.5.<pick any free IP>/32
```

Client configuration example:

```
# /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <paste private key here>
Address = 10.0.59.<same IP you allowed in server's config>/32

[Peer]
PublicKey = <paste public key here>
Endpoint = <paste server's external IP here>:51820
AllowedIPs = 10.0.5.1/24
```

Then you just bring all members up:

```
# Server
wg-quick up wg0

# Clients
wg-quick up wg0
ping 10.0.5.1
```

### Accessing other networks

Probably you would like to forward all traffic through VPN host. Then you need to set `AllowedIPs = 0.0.0.0/0` at the client side as `wg-quick` adds route binded to VPN interface based on this value.

It's also possible to let clients from VPN access some private network. You can't bridge `wg0` interface since it works on L4 of OSI model (using UDP datagrams to send it's own Ethernet frames inside it, check [whitepapers](https://www.wireguard.com/papers/wireguard.pdf) for details), but you're able to setup simple NAT. Client side configuration it this case just needs to be extended with additional subnet and MASQUERADing rules:

```
iptables -t nat -A POSTROUTING -o wg0 -j MASQUERADE

# /etc/wireguard/wg0.conf
...
[Peer]
AllowedIPs = 10.0.5.1/24, 192.168.0.1/24
...
```

### Conclusion

Great solution indeed. :)
