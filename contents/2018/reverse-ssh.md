Date: 2018-03-05 14:36
Category: Technical
Title: SSH host behind NAT
Tags: linux, ssh, autossh

Today I solved task of establishing persistent SSH tunnel from NAT-ted host to local machine.

The problem is that Host B is supplied with dynamic IP, so you can't just connect to it.

```
[A] -X-> [B]
me       target
```

I decided to reverse the process and force Host B to contact my machine (Host A) which has static IP. So Host A now acts as relay/gateway host.

```
[A] <--- [B]
relay    target
```

I used `autossh` tool to sort the things out. First, let's install it and prepare the systemd service file:

```
# /lib/systemd/system/autossh.service

[Unit]
Description=AutoSSH tunnel
After=network.target ssh.service

[Service]
ExecStart=/opt/autossh.sh
Restart=on-failure
User=user # EDIT ME
```

Now we should create some kind of `/opt/autossh.sh` script:

```
#!/bin/bash

export AUTOSSH_DEBUG=yes
export AUTOSSH_LOGFILE=/var/log/autossh.log

autossh -M 10900 -N \
  -o "PubkeyAuthentication=yes" \
  -o "IdentityFile=/home/user/.ssh/id_rsa" \ # EDIT ME
  -o "StrictHostKeyChecking=false" \
  -o "PasswordAuthentication=no" \
  -o "ServerAliveInterval 60" \
  -o "ServerAliveCountMax 3" \
  -R relayhost:9022:localhost:22 user@relayhost # EDIT ME
```

This would start local SSH process on `RELAY:9022` which forwards you to `TARGET:22`.

Then create log file and start the service:

```
touch /var/log/autossh.log
chown user: /var/log/autossh.log # EDIT ME

systemctl enable autossh.service
systemctl start autossh.service
systemctl status autossh.service
```

Now I'm always able to reach Host B by connecting to Host A's port 9022.

Pretty easy.
