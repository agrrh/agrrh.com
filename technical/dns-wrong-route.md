Title: Dig: reply from unexpected source
Date: 2015-09-04 11:25
Tags: dig, dns, routes

Yesterday I tried to dig some hostname from local DNS server and got such result:

    $ dig domain.local.tld @10.0.20.1
    ;; reply from unexpected source: 10.0.0.1#53, expected 10.0.20.1#53

First, let me explain network scheme:

    (clients) --- router --- (inet)
    dns       ---/
    fileshare ---/

- Client is 10.0.99.1
- DNS host is 10.0.20.1
- router is 10.0.0.1
- DNS default route os 10.0.0.1 and it - Clients default route is same 10.0.0.1

The reason was quite simple:

DNS got zero knowledge about 10.0.99.1/24 subnet and answered through 10.0.0.1, specifying it as source.

The solution was just:

    root@dns # ip r add 10.0.99.1/24 dev eth0 src 10.0.20.1

Then I was able to dig local addresses again.
