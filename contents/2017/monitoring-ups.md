Date: 2017-10-15 12:28
Category: Technical
Title: Gathering UPS metrics with NUT and Telegraf
Tags: metrics, telegraf, influx, bash, nut

I'm going to gather metrics from my UPS.

![preview]({filename}/media/ups_metrics.png)

Things I'm using here:

- NUT
- Telegraf
- InfluxDB
- Grafana

So, there's a program called [NUT](http://networkupstools.org/) (Network UPS Tools) which let you gather data from UPS equipped with RS-232/USB data port.

In this case I'm working with IPPON Back Comfo Pro 600 via USB. In command line you use sudo or just impersonate as root user.

First, let's install NUT:

```
apt install nut
```

Now add your UPS config to NUT:

```
# tail -n5 /etc/nut/ups.conf

[ippon]
driver = blazer_usb
port = auto
desc = "IPPON 600 UPS, USB interface"
```

Enable network interface for upsd:

```
# grep ^LISTEN /etc/nut/upsd.conf

LISTEN 127.0.0.1 3493
```

Add upsd user accounts:

```
# cat /etc/nut/upsd.users

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
```

Add monitor entry to upsmon conf.


I'm not going to change any settings or perform any actions so using slave for monitoring and not configuring anything more.

```
# grep ^MONITOR /etc/nut/upsmon.conf

MONITOR ippon@localhost 1 upsslave passwordslave slave
```

Check the things out:

```
# Starting daemon
service nut-server restart

# Checking visibility of my device
upsc -l

# Gathering all the sensitive data
upsc ippon

...
battery.charge: 100
input.voltage: 211.7
output.voltage: 211.7
ups.temperature: 25.0
...
```

Now let's setup Telegraf metrics gathering with this script (should be executable):

```
# cat /opt/ups_metrics.sh

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

You could alternate the script knowing bash syntax and [InfluxData line protocol scpecs](https://docs.influxdata.com/influxdb/v1.3/write_protocols/line_protocol_tutorial/).

Then we add this script as input for our telegraf daemon (which supposed to be setup with proper DB output):

```
# grep -A 4 inputs.exec /etc/telegraf/telegraf.conf

[[inputs.exec]]
  commands = [
    "/opt/ups_metrics.sh"
  ]
  data_format = "influx"
```

Restart the daemon and enjoy your graphs. :)
