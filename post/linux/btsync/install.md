# AS ROOT!
sudo -s

# get binaries
# linux x64
# URL=http://download-lb.utorrent.com/endpoint/btsync/os/linux-x64/track/stable
# linux arm
# URL=http://download-lb.utorrent.com/endpoint/btsync/os/linux-arm/track/stable

wget "$URL" -O - | tar xzvf - btsync
mv btsync /usr/bin/btsync
chown root: /usr/bin/btsync

# prepare autostart script

wget https://agrrh.com/linux/btsync/start_script.sh -O /etc/init.d/btsync
chmod 775 /etc/init.d/btsync
update-rc.d btsync defaults

# add multiple users, if needed
#nano /etc/init.d/btsync

# adding a config

USER=agrrh
mkdir /home/$USER/.sync
wget https://agrrh.com/linux/btsync/config.json -O /home/$USER/.sync/config.json
chown -Rf $USER: /home/$USER/.sync
sed -i "s/USER/$USER/g" /home/$USER/.sync/config.json

# start it! :)
/etc/init.d/btsync start
