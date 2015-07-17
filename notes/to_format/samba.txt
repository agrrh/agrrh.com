# Sharing management

# share example, should go to /etc/samba/smb.conf
# name
[myshare]
  comment = What is this
  path = /fileshare
  # allow for users from group "uesrs"
  valid users = @users
  # new files settings
  force group = users
  create mask = 0660
  directory mask = 0771
  # inherit owner = yes
  # inherit permissions = yes
  writable = yes
  browseable = yes
  guest ok = yes

# Users management

# add user without a home dir to group "uesrs"
useradd -M -G users myuser

# create smb account, set a password
smbpasswd -a myuser

# activate/ disable account
smbpasswd -e myuser
smbpasswd -d myuser

# delete account
smbpasswd -x myuser
userdel myuser

# list users
pdbedit -L
pdbedit -Lv
