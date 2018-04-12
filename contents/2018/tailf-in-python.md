Date: 2018-01-26 00:20
Category: Technical
Title: tail --follow in python
Tags: python

When writing a bot to detect CV visits and notify me via Telegram, I was implementing `tail --follow` in python to evade usage of system's tail utility.

Here is how this generator could be used as separate program:

```
#!/usr/bin/env python

import sys
import time

def tailf(fname):
    try:
        fp = open(fname, 'r')
    except IOError:
        print('Could not open file')
        sys.exit(1)

    fp.seek(0, 2)
    while True:
        line = fp.readline()
        if line:
            yield line.strip()
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        print('File not specified')
        sys.exit(1)

    for line in tailf(fname):
        print(line)
```

Then you do:

```
$ (while true; do date >> file.txt; sleep 1; done) &
$ chmod +x tailfpy
$ ./tailfpy file.txt
Fri Jan 26 00:11:27 MSK 2018
Fri Jan 26 00:11:28 MSK 2018
Fri Jan 26 00:11:29 MSK 2018
```

Voila!
