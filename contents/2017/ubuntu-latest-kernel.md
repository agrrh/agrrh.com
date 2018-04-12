Date: 2017-07-25 17:21
Category: Technical
Title: Ubuntu LTS: Use latest kernel
Tags: ubuntu, kernel, hwe

I was using Ubuntu 16.04 LTS with it's default 4.4 kernel and would like to test [BBR](https://github.com/google/bbr) congestion algorithm which available since 4.10 only.

Solution is very simple due to [LTSEnablementStack/HWE](https://wiki.ubuntu.com/Kernel/LTSEnablementStack) feature. Can't say why, but this feature wasn't enabled at target host, probably it was installed too long ago, before HWE became default option.

```
apt-get install --install-recommends linux-generic-hwe-16.04
```

In case of desktop machine, just add XOrg-related metapackage:

```
apt-get install --install-recommends linux-generic-hwe-16.04 xserver-xorg-hwe-16.04
```

Then reboot the host and it's done:

```
# uname -r
4.10.0-27-generic
```
