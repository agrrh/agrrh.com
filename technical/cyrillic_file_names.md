Title: Dealing with cyrillic names under linux
Date: 2015-08-28 18:18
Tags: mount, convmv, encodings

Fixing question marks in cyrillic file names with `convmv`:

    convmv -f cp1251 -t koi8 -r ./
    convmv -f cp1251 -t koi8 -r ./ --notest

Fix names of files extracted from zip archive, which was created under Windows:

    convmv -f cp1252 -t cp850 ./ --notest
    convmv -f cp866 -t utf-8 ./ --notest

And there's almost the same issue while mounting FAT32 partitions, the solution is to specify codepage and force UTF-8 encoding:

    mount /dev/sdb1 /mnt/test -t vfat -o iocharset=cp1251,codepage=866,utf8=true

Thank you!

References:

- [http://najomi.org/_nix/convmv](http://najomi.org/_nix/convmv)
- [http://www.gamedev.ru/flame/forum/?id=13379](http://www.gamedev.ru/flame/forum/?id=13379)
