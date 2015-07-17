# List physical drives
megacli -PDList -Aall

# Filtered list physical drives
megacli -PDList -Aall | egrep 'Slot|Raw|Inquiry|Device ID|Firmware state'

# Delete config
megacli -CfgLdDel -Lall -aAll
# Clear config, almost the same
megacli -CfgClr -aAll

# Create RAID 1
megacli -CfgLdAdd -r1 [252:0,252:1] WB RA Cached CachedBadBBU -a0

# Create RAID 10
megacli -CfgSpanAdd -r10 -Array0[252:0,252:1] Array1[252:2,252:3] WB RA Cached CachedBadBBU -a0

# Create RAID 5
megacli -CfgLdAdd -r5 [252:0,252:1,252:2,252:3] WB RA Cached CachedBadBBU -a0

# Create RAID 10 of 6 disks
megacli -CfgSpanAdd -r10 -Array0[32:0,32:1] Array1[32:2,32:3] Array2[32:4,32:5] WB RA Cached CachedBadBBU -a0

# Create JBOD of 2nd channel disk
megacli -cfgldadd -r0[252:2] -a0

# List logical drives
megacli -LDInfo -Lall -Aall

# Scan for foreign disks
megacli -CfgForeign -Scan -a0

# Clear foreign disks cfg
megacli -CfgForeign -Clear -a0

# Set alarm
# on
megacli -AdpSetProp AlarmEnbl -aALL
# off
megacli -AdpSetProp AlarmDsbl -aALL
