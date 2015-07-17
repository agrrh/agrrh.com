Title: Perisher
Date: 2015-07-17 13:09
Tags: monitoring, python

Client-server application to monitor overall health of small debian-like hosts group.

[ [GitHub](https://github.com/agrrh-/perisher) ]
[ [latest *.deb](http://perisher.agrrh.com/download/) ]

![preview]({filename}/media/perisher-showoff-host.png)

Advantages/Disadvantages:

- Designed to use without disturbing disks, usually client utilizes zero I/O operations during data collection. Most of the data gathered from RAM.
- Server saves all the data in RAM too, so there's no performance problems on reading with the dozens and thousands of clients.
- Application is not finished yet. Got tons of bugs and issues to work on.
- SQLite could act as bottleneck when there's large number of write operations occurs at the same time.

Technologies used:

- Server: Python3, SQLite
- Client: Python3
- Web interface:
    - Python3, Flask
    - Jinja2
    - jQuery

Kinda useful tool to use at any PAN full of Debian boxes.
