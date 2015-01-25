#!/bin/bash
/etc/init.d/apache2 restart
/etc/init.d/httpd restart
/etc/init.d/nginx restart
/etc/init.d/lighttpd restart
/etc/init.d/postfix restart
/etc/init.d/proftpd restart
/etc/init.d/vsftpd restart 
/etc/init.d/dovecot restart
if pidof /usr/local/ispmgr/sbin/ihttpd > /dev/null; then
    ISP_PID=$(pidof /usr/local/ispmgr/sbin/ihttpd)
    ISP_COMMAND=$(ps -o cmd -p  $ISP_PID | tail -1)
    kill -9 $ISP_PID
    exec $ISP_COMMAND
fi
