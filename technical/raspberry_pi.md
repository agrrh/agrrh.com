Title: Raspberry PI recipes
Date: 2015-07-17 18:18
Tags: raspberry pi, watchdog, fork bomb

All recipes here related to Raspbian OS.

##### Change Raspberry PI MAC

Add this argument (not as new line, just continue one which already present!) to the end of `/boot/cmdline.txt`:

    smsc95xx.macaddr=00:00:00:00:00:01

##### Disable screensaver

Just add those to any executable script and run.

    @xset s off
    @xset -dpms
    @xset s noblank

For example, `~/.xsessionrc` would be fine.

##### Enable sound on headless Raspberry

Enable sound output in the kernel:

    echo "hdmi_drive=2" >> /boot/config.txt
    echo "snd_bcm2835 " >> /etc/modules

Install audio controls and player:

    apt-get install alsa-utils moc

    sudo amixer cset numid=3 1 # 0=auto, 1=headphones, 2=hdmi
    alsamixer

Now play something with mocp:

    mocp

##### Watchdog to reboot hung Raspberry

There's two parts of watchdog in Raspberry Pi - hardware one integrated with SoC and software daemon.

First we would enable hardware one, to do so you need to load the kernel module:

    # modprobe bcm2708_wdog
    # echo "bcm2708_wdog" >> /etc/modules

Then configure it:

- nowayout=1 - watchdog could not be stopped by other processes
- heartbeat=12 - number in seconds to wait for activity and reset if there's no any


    echo "options bcm2708_wdog nowayout=1 heartbeat=12" >> /etc/modprobe.d/watchdog.conf

Now install the software part:

    # apt-get install watchdog
    # update-rc.d watchdog defaults

Enable one of conditions in `/etc/watchdog.conf`, looks like most reliable is `max-load-1`:

    max-load-1 = 24

Probably you also want to disable `realtime` and `priority` values in config. Otherwise it's possible that system is still running pretty inoperable, but because watchdog daemon has such a high priority, it is happy. See related [stackexchange](http://raspberrypi.stackexchange.com/questions/3732/watchdog-daemon-not-restarting-pi-after-fork-bomb) topic.

Then just reboot the host:

    # reboot

You could also want to check watchdog by doing fork bomb or just killing the process:

    swapoff -a
    :(){ :|:& };:

    kill -9 $(pidof watchdog)

Server should stop responding and after few moment go for a reboot.
