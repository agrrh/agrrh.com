SWAP_GB=2

dd if=/dev/zero of=/swap bs=1024 count=$[$SWAP_GB*1024*1024]
mkswap /swap
chown root:root /swap
chmod 0600 /swap

free -m
swapon /swap 
free -m

echo "/swap swap swap defaults 0 0" >> /etc/fstab
