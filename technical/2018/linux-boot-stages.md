Title: Linux boot stages
Date: 2018-01-24 01:29
Tags: linux, mbr, grub, init, boot, kernel

How does linux boots up, from power button to running services.

#### Power button

When you pressed power button, current runs through circuits over the motherboard and boot process starts.

It also could be magic packet sent via network or some other remote start method. Let's say, command sent from IPMI.

#### Motherboard low-level software

Thus used to be called BIOS. For modern PCs UEFI is used.

[BIOS](https://en.wikipedia.org/wiki/BIOS) stands for Basic Input/Output System and [UEFI](https://en.wikipedia.org/wiki/Extensible_Firmware_Interface) means Unified Extensible Firmware Interface.

The main difference is that UEFI is small OS while BIOS is just a kind of firmware or a program built right on top of firmware.

UEFI is newer standard and supports actual technologies, like fancy graphics, secure boot, 3TB HDDs (thanks, GPT), more than 1MB of memory, networking and so on.

Both of these programs seek for bootloader inside HDD's MBR and try to execute it.

#### Master Boot Record

Master Boot Record is just a place on hard disk where location of bootloader is stored.

In newer systems, GPT could used to store such information. Conceptually it's same process of transferring control to bootloader, but it defers in how data is organized and which limits are applied.

#### GRUB

GRUB stands for Grand Unified Bootloader.

It's what let you choose which one from multiple kernel images to use. Also could just silently start default one or let you perform memory check without actually booting main OS.

GRUB boots in few stages:

- Stage 1: While posessing low amount of memory, it knows what disk is. It reads `boot.img` from MBR and point process to begin `core.img`.
- Stage 1.5: `core.img` contains knowledge about partitions. Here we load file system drivers needed to properly continue.
- Stage 2: We now know about file systems and could read kernel images list and display user a menu to select desired one.

GRUB loads and executes kernel and initrd image.

#### Kernel and initrd

We mount file system stated in selected GRUB menu entry.

Initrd stands for Initial RAM Disk. This is temporary filesystem used to store executables, additional drivers or modules modules which are critical for boot process. In embedded systems it could be never unloaded and stays in use as root file system.

So, kernel was loaded. Then it loads initrd, use resources stored inside to mount actual root file system and unloads initrd image.

Then kernel runs /sbin/init as PID 1 process.

#### Init

Init is main program which runs other processes. Could be replaced with upstart, systemd or others.

System V Init reads `/etc/inittab` file to decide which run level to start:

```
0 Halt
1 Single user mode
2 Multi-user mode, w/o networking
3 Multi-user mode
4 -
5 Graphical mode
6 Reboot
```

Other initialization systems use other files so don't be confused if you don't find `/etc/inittab`.

So, for server machine you probably boot to runlevel 3 and workstation usually boots to runlevel 5.

#### Running services

This is where all of your actual software is started.

Various init systems use various files to determine exact order (and dependencies in case if it's flexible enough) in which software should be run.

Init uses `/etc/rc?.d/` directories.
Upstart uses files from `/etc/init/` directory.
Systemd relies on files inside `/etc/systemd/`.

That's basically how Linux boot process happens.

Links:

- [Linux boot process](https://www.thegeekstuff.com/2011/02/linux-boot-process)
- [GRUB](https://en.wikipedia.org/wiki/GNU_GRUB)
- [Initrd](https://www.opennet.ru/base/sys/initrd_intro.txt.html)
- [Init](https://en.wikipedia.org/wiki/Init)
- [Systemd](https://en.wikipedia.org/wiki/Systemd)
