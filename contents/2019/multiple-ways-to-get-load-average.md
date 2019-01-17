Date: 2019-01-17 10:52
Category: Technical
Title: 5 ways to check load average
Tags: linux

>All roads lead to Rome.
>
> -- medieval statement

One of most popular questions during technical interview:

### What is load average?

This is just representation of system load. Some kind of processes queue exposed by scheduler.
```
$ cat /proc/loadavg
0.61 0.81 0.84 1/1162 15359
```
Those values show average number of processes waiting in latest 1/5/15 minutes: `0.61 0.81 0.84`.

`1/1162` tells us that only 1 of total 1162 processes is executed at the moment.

Finally, `115359` is latest PID allocated by the kernel.

Okay, next popular question is:

### Propose multiple ways to check current LA

Most common answer is something like:

- Execute `cat /proc/loadavg`
- `grep` from `w` / `uptime` utilities
- Run `top` / `htop` or `tload`
- `getloadavg()` from glibc
- some other language-specific functions like Python `os.getloadavg()`

All those ideas (but first one!) is a crap. There's only 1 way to check for LA - reading `/proc/loadavg`.

- All of `w`, `uptime`, `tload` and `top` use psproc lib which [read it from this file](https://gitlab.com/procps-ng/procps/blob/920b0ada70e9c3137505c2645c67f4f63dc79c50/proc/sysinfo.c#L446-463).
- [Same for `htop`](https://github.com/hishamhm/htop/blob/666e1e76b39ee66a38f5fb620d22b23f36859eca/linux/Platform.c#L143-L154) and family.
- Even glibc [uses same file](https://github.com/lattera/glibc/blob/688903eb3ef01301d239ab753d309d45720610a7/sysdeps/unix/sysv/linux/getloadavg.c#L36).
- And, finally, Python [calls for glibc's](https://github.com/python/cpython/blob/438b534ad0e7522cadba20cd3aec41d02b2bc09b/Modules/posixmodule.c#L7146-L7156) `getloadavg()`, which reads same file again.

In fact, there's only one way to check for load average values.
