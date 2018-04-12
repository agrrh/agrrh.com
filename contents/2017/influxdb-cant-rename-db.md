Date: 2017-09-25 23:05
Category: Technical
Title: InfluxDB can't rename database
Tags: influxdb, metrics

I got InfluxDB with a year of statistical data about how my server's lifetime goes.

For historical reasons I was using UDP protocol to store data, so there was no authorization above it. After all, it was local data transport inside my PAN. So, DB was named "udp".

Now I started to use it as database for storing data from few hosts so I've disabled UDP transport and enabled HTTP one with basic authorization (TCP, of course, we're still not ready for using QUIC). So I decided to rename database from "udp" to let's say "main_and_only_database_to_store_metrics".

And there it became clear that InfluxDB just can't rename databases, here's a [related issue](https://github.com/influxdata/influxdb.com/issues/384).

This is awful. Looks like feature was implemented but then became obsolete due to bugs or something.

I ended up just dropping my old database and creating new one instead, there was zero sensitive data anyways, but overall situation is horrible.

Production-ready, my ass.
