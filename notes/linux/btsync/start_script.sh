#!/bin/sh
### BEGIN INIT INFO
# Provides: btsync
# Required-Start: $local_fs $remote_fs
# Required-Stop: $local_fs $remote_fs
# Should-Start: $network
# Should-Stop: $network
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Multi-user daemonized version of btsync.
# Description: Starts the btsync daemon for all registered users.
### END INIT INFO

# Replace with linux users you want to run BTSync clients for
BTSYNC_USERS="agrrh"
DAEMON=/usr/bin/btsync

start() {
  for btsuser in $BTSYNC_USERS; do
    HOMEDIR=`getent passwd $btsuser | cut -d: -f6`
    config=$HOMEDIR/.sync/config.json
    if [ -f $config ]; then
      echo "Starting BTsync for $btsuser"
      start-stop-daemon -b -o -c $btsuser -S -u $btsuser -x $DAEMON -- --config $config
    else
      echo "Couldn't start BTsync for $btsuser (no $config found)"
    fi
  done
}

stop() {
  for btsuser in $BTSYNC_USERS; do
    dbpid=`pgrep -fu $btsuser $DAEMON`
    if [ ! -z "$dbpid" ]; then
      echo "Stopping BTsync for $btsuser"
      start-stop-daemon -o -c $btsuser -K -u $btsuser -x $DAEMON
    fi
  done
}

status() {
  for btsuser in $BTSYNC_USERS; do
    dbpid=`pgrep -fu $btsuser $DAEMON`
    if [ -z "$dbpid" ]; then
      echo "BTsync for USER $btsuser: not running."
    else
      echo "BTsync for USER $btsuser: running (pid $dbpid)"
    fi
  done
}

case "$1" in
 start)
start
;;
stop)
stop
;;
restart|reload|force-reload)
stop
sleep 2
start
;;
status)
status
;;
*)
echo "Usage: /etc/init.d/btsync {start|stop|reload|force-reload|restart|status}"
exit 1
esac

exit 0