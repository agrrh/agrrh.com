# lvm2
# 
# http://www.centos.org/docs/5/html/Cluster_Logical_Volume_Manager/

# There's 3 abstraction levels:
# 1 Physical volume
# 2 Volume groups
# 3 Logical volume

# at first you should erase partition table
dd if=/dev/zero of=/dev/TARGET bs=512 count=1

# create Physical Volumes (PV)
pvcreate /dev/sda1
# also you could use software raids and so on ...
# pvcreate /dev/md2

# examine PVs
pvscan
pvdisplay

# create Volume Group (VG) with number of PVs
# one
vgcreate vg1 /dev/md3
# or few
vgcreate vg1 /dev/sda1 /dev/sdb1

# create LV
lvcreate -n $NAME -L10G vg1

# look at the baby :)
lvdisplay

# add PV to VG
vgextend vg1 /dev/sdc1

# move data from one to another
pvmove /dev/sda1 /dev/sdc1

# and remove one from the group
vgreduce vg1 /dev/sda1

# remove missing
vgreduce --removemissing [--force] vg1
