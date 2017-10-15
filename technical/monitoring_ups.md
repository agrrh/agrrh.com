Title: Gathering UPS metrics with NUT and Telegraf
Date: 2017-10-15 12:28
Tags: metrics, telegraf

I'm going to gather metrics from my UPS.

![preview]({filename}/media/ups_metrics.png)

Things I'm using here:

- NUT
- Telegraf
- InfluxDB
- Grafana

So, there's a program called [NUT](http://networkupstools.org/) (Network UPS Tools) which let you gather data from UPS equipped with RS-232/USB data port.

In this case I'm working with IPPON Back Comfo Pro 600 via USB.

```
# Here you work as root user or using sudo

# Install NUT
apt install nut

# Add your UPS config to NUT
tail -n5 /etc/nut/ups.conf

[ippon]
driver = blazer_usb
port = auto
desc = "IPPON 600 UPS, USB interface"

# Enable network interface for upsd
grep ^LISTEN /etc/nut/upsd.conf

LISTEN 127.0.0.1 3493

# Add upsd user accounts
cat /etc/nut/upsd.users

[upsmaster]
        password = passwordmaster
        allowfrom = localhost
        upsmon master
[upsslave]
        password = passwordslave
        allowfrom = localhost
        upsmon slave
[upsadmin]
        password = passwordadmin
        allowfrom = localhost
        actions = SET
        instcmds = ALL

# Add monitor entry to upsmon conf
#   I'm not going to change any settings or perform any actions
#   so using slave for monitoring and not configuring anything more
grep ^MONITOR /etc/nut/upsmon.conf

MONITOR ippon@localhost 1 upsslave passwordslave slave

# Starting daemon
service nut-server restart

# Checking visibility of my device
upsc -l

# Gathering all data
upsc ippon

Init SSL without certificate database
battery.charge: 100
battery.voltage: 13.70
battery.voltage.high: 13.00
battery.voltage.low: 10.40
battery.voltage.nominal: 12.0
device.type: ups
driver.name: blazer_usb
driver.parameter.pollinterval: 2
driver.parameter.port: auto
driver.version: 2.7.2
driver.version.internal: 0.11
input.current.nominal: 2.0
input.frequency: 50.0
input.frequency.nominal: 50
input.voltage: 211.7
input.voltage.fault: 211.7
input.voltage.nominal: 220
output.voltage: 211.7
ups.beeper.status: enabled
ups.delay.shutdown: 30
ups.delay.start: 180
ups.load: 34
ups.productid: 5161
ups.status: OL
ups.temperature: 25.0
ups.type: offline / line interactive
ups.vendorid: 0665

# Filter only important data
upsc ippon | grep -E '^(battery.charge|input.voltage|output.voltage|ups.temperature): ' | cut -d ' ' -f2

100
214.2
214.2
25.0
```

Now let's setup Telegraf metrics gathering with this script (should be executable):

```
cat /opt/ups_metrics.sh

#!/bin/bash

UPS_NAME="ippon"

GATHER_COMMAND="upsc ${UPS_NAME}"

(
  M_CHARGE=$(${GATHER_COMMAND} | grep battery.charge | cut -d' ' -f2)
  M_INVOLT=$(${GATHER_COMMAND} | grep input.voltage | cut -d' ' -f2)
  M_OUTVOLT=$(${GATHER_COMMAND} | grep output.voltage | cut -d' ' -f2)
  M_TEMPERATURE=$(${GATHER_COMMAND} | grep ups.temperature | cut -d' ' -f2)

  # cpu,host=server01,region=uswest value=1 1434055562000000000
  METRICS="charge_perc=${M_CHARGE},input_v=${M_INVOLT},output_v=${M_OUTVOLT},temp=${M_TEMPERATURE}"

  echo ups,host=$(hostname --fqdn),ups=${UPS_NAME} ${METRICS} $(date +%s)
) 2>/dev/null
```

You could alternate the script knowing [InfluxData line protocol scpecs](https://docs.influxdata.com/influxdb/v1.3/write_protocols/line_protocol_tutorial/).

Then we add this script as input for our telegraf daemon (which supposed to be setup with proper DB output):

```
grep -A 4 inputs.exec /etc/telegraf/telegraf.conf

[[inputs.exec]]
  commands = [
    "/home/agrrh/.scripts/ippon_telegraf_metrics.sh"
  ]
  data_format = "influx"
```

Restart the daemon and enjoy your graphs. :)
