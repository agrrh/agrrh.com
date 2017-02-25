Title: Java and Timezone
Date: 2015-07-18 09:55
Tags: java, timezone, debian

А у меня будет своя таймзона, с преферансом и куртизанками.

>While most application software will use the underlying operating system for timezone information, the Java Platform, from version 1.3.1, has maintained **its own timezone database**. This database is updated whenever timezone rules change. Oracle provides an updater tool for this purpose.

В общем, если временная зона в Java-приложении кажется некорректной, имеет смысл проделать следующее:

1. Проверить:

    - `/etc/localtime` должен быть линкой/копией файла зоны.
    - `/etc/timezone` должен просто содержать строку, указывающую на зону, например: `Europe/Moscow`.

Практика показывает, что иногда (ubuntu precise, кажется) система может обносить только первый файл и Java будет получать устаревшие настройки, кря.

2. Воспользоваться утилитой TZUpdater, которая может быть найдена тут:

    [http://www.oracle.com/technetwork/java/javase/tzupdater-readme-136440.html](http://www.oracle.com/technetwork/java/javase/tzupdater-readme-136440.html)
    [http://www.oracle.com/technetwork/java/javase/downloads/index.html](http://www.oracle.com/technetwork/java/javase/tzupdater-readme-136440.html)

К сожалению, причины такой поломки остались неизвестны. Скорее всего, приветы надо передавать ansible тогда еще версий 1.x и только-только мигрировавшему на него отделу.
