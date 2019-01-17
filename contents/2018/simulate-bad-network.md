Date: 2018-10-24 23:52
Category: Technical
Title: Simulate packet loss and delays
Tags: iptables, network, tc

It was neccessary to test failover script which should switch uplink in case of main ISP outage.

First thing is to just plug the cable out. But how to simulate high RTT and packet losses?

Here comes traffic control (`tc`) utility with it's queuing disciplines (`qdisc`). Long story short, it let you control how your traffic goes trough interfaces.

Let's start with adding 100ms to every packet:

```
tc qdisc ls dev eth0

tc qdisc add dev eth0 root netem delay 100ms

<perform your tests>

tc qdisc del dev eth0 root netem delay 100ms
```

It's also possible to add different delays based on RNG:

```
# from 500ms to 1500ms
tc qdisc add dev eth0 root netem delay 1000ms 500ms

#
tc qdisc add dev eth0 root netem delay 2000ms 500ms 25%
```

Let's then simulate packet loss:

```
tc qdisc change dev eth0 root netem loss 1%

# Same via iptables
# iptables -A INPUT -m statistic --mode random --probability 0.01 -j DROP

# and more random distribution
tc qdisc change dev eth0 root netem loss 1% 25%
```

Voila, we can simulate network issues now.

See more detailed descriptions and examples here: https://wiki.linuxfoundation.org/networking/netem#packet-loss
