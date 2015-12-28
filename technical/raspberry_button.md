Title: Raspberry PI button
Date: 2015-12-11 19:39
Tags: raspberry pi, gpio

I managed to attach a button to simple Raspberry PI case and here's the script to read it's state:

    #!/bin/bash

    function read_gpio()
    {
      local result=$[1 - $(gpio -g read 8)]
      echo $result
    }

    function reset_gpio()
    {
      gpio -g mode 7 out
      gpio -g mode 8 in

      gpio -g write 7 0
      gpio -g write 8 1
    }

    reset_gpio

    if [[ "$1" == "read" ]]; then
      read_gpio
    fi

    if [[ "$1" == "run" ]]; then
      if [ ! -f "$2" ]; then
        echo "Could not find script file: \"$2\""
        exit 1
      fi

      echo "started" 1>&2

      VAL=0

      while [ true ]; do
        PREV_VAL=$VAL
        VAL=$(read_gpio)
        if [ "$PREV_VAL" -eq "0" ] && [ "$VAL" -eq "1" ]; then
          echo "triggered" 1>&2
          bash $2
        fi
        sleep 0.2
      done
    fi

One probably gonna use it like this:

    # /etc/rc.local
    screen -dmS button bash /opt/button.sh run /opt/button_action.sh

Notice, this was tested with sleep ver 8.13, older versions could not support float.
