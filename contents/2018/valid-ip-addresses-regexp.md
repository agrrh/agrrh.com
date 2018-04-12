Date: 2018-02-21 20:37
Category: Technical
Title: Regular expression for validating IP addresses
Tags: python, ipv4

Let's say, we would like to determine if particular symbols are valid public IPv4 address.

```
# valid octet, 0-255
octet = '1?[0-9][0-9]?|2([0-4][0-9]|5[0-5])'

# 4 valid octets separated with dots
octet_with_dot = octet + '\.'

# IPv4-address
ip_regex = '^({a}){3}{b}$'.format(a=octet_with_dot, b=octet)
```

But does it belong to public IPv4 address space?

```
# private addresses
10.0.0.0    .. 10.255.255.255
172.16.0.0  .. 172.31.255.255
192.168.0.0 .. 192.168.255.255

# multicast addresses
224.0.0.0   .. 239.255.255.255
```

So, we should exclude addresses starting with those prefixes. Let's use Python for this:

```
import re

def public_ip_address_test(probably_ip):
    octet = '1?[0-9][0-9]?|2([0-4][0-9]|5[0-5])'
    octet_with_dot = octet + '\.'
    ip_regex = '^({a}){3}{b}$'.format(a=octet_with_dot, b=octet)

    prefixes_to_exclude = (
        '^10\.',
        '^172\.1[6-9]\.',
        '^172\.(2[0-9]|3[01])\.',
        '^192\.168\.',
        '^224\.(1?[0-9][0-9]?|2([0-3][0-9])\.'
    )

    if not re.match(ip_regex, probably_ip):
        return False

    for bad_prefix in prefixes_to_exclude:
        bad_prefix = '^' + bad_prefix
        if re.match(bad_prefix, probably_ip):
            return False

    return True
```

Voila.

And yes, you'd better to use `ipaddr` module to perform such checks.
