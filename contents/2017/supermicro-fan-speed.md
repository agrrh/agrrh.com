Date: 2017-10-26 22:15
Category: Technical
Title: Controlling fan speed on SuperMicro server
Tags: supermicro, ipmitool, hardware

I'm using [SuperMicro 5018A-MHN4](http://www.supermicro.com/products/system/1U/5018/SYS-5018A-MHN4.cfm) as my router, fileshare host, virtualization and web server.

Since I monitor it's overall health parameters, such as temperature, it opens a way to advanced server systems control. For example, it's a good idea to slow down the fans while host is cool and speed em up when things got hot.

This is how to control overall policy:

```
# Show current mode

ipmitool raw 0x30 0x45 0x00

# 0x00 - Standard
# 0x01 - Full
# 0x04 - Heavy I/O

# Set new mode
ipmitool raw 0x30 0x45 0x01 0x??
```

Same as you could set via web panel.

And here's a way to tune fans speed deeper:

```
# 0x00 ~ 2500 RPM
# 0x04 ~ 3100 RPM
# ..
# 0x64 ~ 13200 RPM

ipmitool raw 0x30 0x70 0x66 0x01 0x00 0x??
```

Thanks to [this guy's post](https://forums.servethehome.com/index.php?resources/supermicro-x9-x10-x11-fan-speed-control.20/).
