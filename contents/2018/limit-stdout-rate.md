Date: 2018-05-12 20:49
Category: Technical
Title: Limit backup disk usage rate
Tags: linux, stdout, pv, pipe, mongodump, mysqldump

Sometimes you don't want to utilize disk too heavy.

My case was not to alert monitoring on disk i/o trigger (and yes, this is a workaround, in common case you'd probably like to modify alert setting instead). I tried `nice`, `ionice` and even `systemd-run -p "IOWriteBandwidthMax=/dev/sdX 10M"`, but got no luck.

Here's a solution with a great `pv` util:

```
mysqldump           ... | pv -q --rate-limit 10M > dump.file
mongodump --archive ... | pv -q --rate-limit 10M > dump.file
```

Also consider using `gzip` or `pigz` (which is able to use multiple processing units) to compress resulting output.
