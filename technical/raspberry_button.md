Title: Raspberry PI button
Date: 2015-12-11 19:39
Tags: raspberry pi, gpio

I managed to attach a button to simple Raspberry PI case and here's the simple script to read it's state:

    # should be ran as root
    
    #!/bin/bash

    ## Author: Kirill K
    ## Description: Script to handle big red button, returns 0 for idle or 1 for pressed state
    ## Usage: button.sh prepare; button.sh

    if [ $1 == "prepare" ]; then
        # prepare out
        if [ ! -d /sys/class/gpio/gpio7 ]; then
            echo 7 > /sys/class/gpio/export
        fi
        echo 1 > /sys/class/gpio/gpio7/value

        # prepare in
        if [ ! -d /sys/class/gpio/gpio8 ]; then
            echo 8 > /sys/class/gpio/export
        fi
        echo 0 > /sys/class/gpio/gpio8/value
    else
        cat /sys/class/gpio/gpio8/value
    fi

One probably gonna use it like this:

    # /etc/rc.local
    bash /opt/button.sh prepare
    while [ true ]; do
        if [ "$(bash /opt/button.sh get)" == "1" ]; then
            # do something
        fi
        sleep 0.5
    done

Tested with sleep ver 8.13, older versions could not support float.

Also, consider some trigger delay handling here, you don't want to send 3 alarm emails for 1.5 sec button press, right?
