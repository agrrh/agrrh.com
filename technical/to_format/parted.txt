# format disk with 3 partitions
# / - 40G
# lvm - 60G
# swap - rest of space
parted /dev/sda mkpart primary ext3 0 40G
parted /dev/sda mkpart primary ext3 40G 100G
parted /dev/sda mkpart primary linux-swap 100G 100%

# make filesystems
mkfs.ext4 /dev/sda1
parted /dev/sda set 2 lvm on
mkswap /dev/sda3

# watch how it worked
fdisk -l /dev/sda
