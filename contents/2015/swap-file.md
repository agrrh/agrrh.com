Date: 2015-07-17 11:59
Category: Technical
Title: Swap in a file
Tags: swap, linux
Summary: Fast and simple way to get some swap space without reboot

Let's say you got no swap partition, but want to use some swap space.

Here's fast and simple way to do so without a reboot.

Create empty image file of desired size:

    # SWAP_GB=2
    # dd if=/dev/zero of=/swap bs=1024 count=$[$SWAP_GB*1024*1024]

Format it as swap space, do the permissions routine:

    # mkswap /swap
    # chmod 0600 /swap

And then see the magic:

    # free -g
    # swapon /swap
    # free -g

Voila!

Don't forget to mount it at permanent basis:

    # echo "/swap swap swap defaults 0 0" >> /etc/fstab

Not a single reboot was given. :)
