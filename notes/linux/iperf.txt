# network speed testing

# server 1 - 1.2.3.4
# server 2 - 5.6.7.8

# IPv4
# testing data transfer speed from server 1 to server 2
# from server 2
iperf -s -u
# from server 1
iperf -u -b 100M -c 1.2.3.4

# outputs following:
[  3] local 185.4.75.51 port 44271 connected with 178.63.65.206 port 5001
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0-10.0 sec    118 MBytes  99.0 Mbits/sec
[  3] Sent 84412 datagrams
[  3] Server Report:
[  3]  0.0-10.1 sec  17.2 MBytes  14.3 Mbits/sec  3.097 ms 72146/84411 (85%)
[  3]  0.0-10.1 sec  1 datagrams received out-of-order
# almost success :)

# IPv6
# server 2
iperf -V -s -u -B 2a01:4f8:121:42e::2
# server 1
iperf -V -u -c 2a01:4f8:121:42e::2 -b 100M