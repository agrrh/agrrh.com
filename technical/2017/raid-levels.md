Title: RAID levels
Date: 2017-09-16 15:10
Tags: raid, data protection

There was a time I was working about a month or two in a small IT company VIST SPb. During those time I wrote an article about [RAID array levels](https://www.vist-spb.ru/articles/25-raid-massivy.html). Now let me repeat it here in english just to refresh this knowledge.

So, RAID is acronym for "redundant array of independent disks". The main idea is to unite number of hardware storage items in one logical item. The algorithm of storing and distributing data across those hardware disks indicates the "RAID level".

It's quite simple to organize such array without any special hardware, there are many ways to do so using software level only:

- [mdadm](https://en.wikipedia.org/wiki/Mdadm)
- [btrfs](https://en.wikipedia.org/wiki/Btrfs)
- number of integrated utilities varying from one OS to another

One should remember that software solutions requires a little bit of CPU time at host machine (not much, it's just XOR operations, after all). Software RAID is still more reliable in case of hardware failure, user can easily move disks to another host and restore array functionality there.

Hardware RAID controllers almost always integrated in server-grade machines. I was using following utilities to manage such arrays:

- LSI megacli
- Adaptec arcconf

In my practice, I faced HW controller failures few times and every time it was a huge pain attempting restore the data.

So, let's talk about most popular RAID levels now:

## RAID 0

This is just a number of disks, sharing sum of volumes capacity into single larger volume.

```
ABCD         ABCD
/  \       / |  | \
A  B      A  B  C  D
C  D      E  F  G  H
```

You got increaced read/write speed, but, of course, you got no any data backup, so every disk failure leads to array rebuild and data restoration procedures.

## RAID 1

Is as simple as "mirroring", each of disks stores same data to prevent it's loss in case of single disk failure.

```
ABCD         ABCD
/  \       / |  | \
A  A      A  A  A  A
B  B      B  B  B  B
C  C      C  C  C  C
```

Probably it's my favorite RAID setup due to it's simplicity. It's still possible to face both disks failure (and I saw it happened few times), so not the best option to store really important data.

## RAID 5

This setup represents striping with parity:

```
  ABCDE
/ | | | \
A B C D x
E F G x H
I G x K L
```

Let's say second disk got faulty. Then data from other disks used to re-generate missing data and it's possible to write it to replaced disk. Data restoration occurs using parity bits "x" with XOR operation. It is possible due to nature of XOR:

```
A xor B xor C = D
A xor B xor D = C
A xor D xor C = B
D xor B xor C = A
```

It is always possible to restore one of operands values using XOR while you know all the rest of operands. Total number of operands doesn't matter here.

## RAID 10

Is a case of RAID0 with RAID1 under the hood. Minimal setup consists of 4 disks:

```
RAID 10      ABCD
             /  \
RAID 0       A  B
             C  D
           / |  | \
RAID 1    A  A  B  B
          C  C  D  D
```

It saves data until at least 1 disk in each pair is alive.

I faced other RAID levels too rare in my career to describe them with competence trusty enough.
