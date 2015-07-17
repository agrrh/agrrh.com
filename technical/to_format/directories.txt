/

This is called root partition. All files and directories start with root partition. Write privileges under this directory are avaible with root user only. Not to confuse it with root user’s home directory, know the difference, “/” is root partition while root user’s home directory is “/root”.

/bin

This directory has binary executable files. Linux commands used in single user mode are found in this directory. It also holds commands that are used by all users. Examples: ls, ping, cp.

/sbin

Like /bin, /sbin also contains binary executable files but the commands held by this directory are used by system administrators with the prime purpose of system maintenance. Examples: iptables, reboot, fdisk.

/etc

It holds all the configuration files which are required by all programs. Shell scripts needed by programs to start or stop them are held by this very directory. Examples are /etc/resolv.conf, /etc/logrotate.conf

/dev

/dev contains device files. In Linux, everything is a file. Included are terminal device or usb or any other device connected to the computer. For example: /dev/usbmon0

/proc

All the system process information is held in /proc. It is a pseudo filesystem as it contains information about running processes. For an instance, /proc/ is the directory which holds information of the process with . It contains information about the system resources. /proc/uptime is one such directory.

/var

var denotes variable files. Those files are kept in this directory that are supposed to grow. Some of the files that reside in here are- /var/log (system log files), /var/lib (package files), /var/mail (emails), /var/spool (print queues), /var/tmp (temporary files that are needed across reboots).

/tmp

System generated and user generated temporary files are kept in this category. Important files should not be saved in here because contents of /tmp are flushed every time system boots.

/usr

/usr is the one that holds user programs. It contains documentations, libraries and source-code for all the second level applications. /usr/bin holds binaries for user programs. While looking for a binary after /bin also look in /usr/bin. Examples of binaries you mighht find in /usr/bin are awk, less, cc. Similarly binary files for system administrators are kept in /usr/sbin. Examples are cron, sshd, useradd. Libraries for /usr/bin and /usr/sbin are kept in /usr/lib. /usr/local holds user programs that a user installs from source.

/home

All user’s personal files are kept in their respective home directories.

/boot

This directory has boot loader files. While booting, files needed are found in /boot. Kernel initrd, grub and few more files reside in this directory.

/lib

Binaries located in /bin and /sbin are supported by library files kept in /lib. Library nomenclature goes like ld* or lib*.so.* . For example: ld-2.11.1.so

/opt

/opt is for add-on optional applications from individual vendors. All applications that are optional should be installed in /opt or any of its subdirectory.

/mnt

/mnt is our mount directory. It is the temporary mount location where where system administrators can mount temporary filesystems.

/media

It serves as the temporary mount point for removable devices. All removable devices are mounted in this directory. Example: /media/cdrom or /media/floppy.

/srv

srv denotes service. All the service related data used for servers is saved in this directory.
