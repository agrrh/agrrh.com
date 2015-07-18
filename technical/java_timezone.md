Title: Java and Timezone
Date: 2015-07-18 09:55
Tags: java, timezone

*I'm going to build my own time zones with blackjack and hookers*

>While most application software will use the underlying operating system for timezone information, the Java Platform, from version 1.3.1, has maintained **its own timezone database**. This database is updated whenever timezone rules change. Oracle provides an updater tool for this purpose.

So, if Java timezone settings looks wrong - one gonna need to check these conditions:

1. Use TZUpdater tool which could be represented and downloaded here:

    http://www.oracle.com/technetwork/java/javase/tzupdater-readme-136440.html

    http://www.oracle.com/technetwork/java/javase/downloads/index.html

2. Check both of the system timezone-related files:

    - `/etc/localtime` should be linked to (or be a copy of) timezone file.
    - `/etc/timezone` should just contain a string that specifies the current timezone, for me it usually should be `Europe/Moscow`.

Practice says that sometimes system updates only first one and Java still gets the wrong tz settings.
