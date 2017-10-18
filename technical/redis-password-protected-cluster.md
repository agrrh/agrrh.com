Title: Setting up Redis password-protected cluster with RCM
Date: 2017-10-18 08:59
Tags: redis, cluster, rcm, ansible, lxd

So, let's say we would like to set up Redis cluster and make it password-protected.

First case could be easily googled to [official docs](https://redis.io/topics/cluster-tutorial), but looks like there's no way to protect your brand new cluster with a password, except [hacking redis-trib.rb](https://trodzen.wordpress.com/2017/02/09/redis-cluster-with-passwords/).

Nope! There is one!

Meet [rcm](https://github.com/maiha/rcm.cr) utility!

It is written in [Crystal](http://crystal-lang.org/) and supposed to be kinda unstable cause of language "alpha" status, but seems to be OK and was tested by me for most common cases.

- First, download binary file from [releases page](https://github.com/maiha/rcm.cr/releases). Better place it somewhere inside `${PATH}`, as calling it as `./rcm` would result in error, you need to call it like just `rcm`.

- Make sure you've set up redis cluster, here I use LXD and Ansible to simplify things out:

```
$ for i in $(seq 1 6); do
  lxc launch ubuntu: lxdhost:redis${i};
done

$ lxc list lxdhost:
+--------+---------+---------------------+------+------------+-----------+
|  NAME  |  STATE  |        IPV4         | IPV6 |    TYPE    | SNAPSHOTS |
+--------+---------+---------------------+------+------------+-----------+
| redis1 | RUNNING | 10.1.101.105 (eth0) |      | PERSISTENT | 0         |
+--------+---------+---------------------+------+------------+-----------+
| redis2 | RUNNING | 10.1.101.135 (eth0) |      | PERSISTENT | 0         |
+--------+---------+---------------------+------+------------+-----------+
| redis3 | RUNNING | 10.1.101.100 (eth0) |      | PERSISTENT | 0         |
+--------+---------+---------------------+------+------------+-----------+
| redis4 | RUNNING | 10.1.101.114 (eth0) |      | PERSISTENT | 0         |
+--------+---------+---------------------+------+------------+-----------+
| redis5 | RUNNING | 10.1.101.125 (eth0) |      | PERSISTENT | 0         |
+--------+---------+---------------------+------+------------+-----------+
| redis6 | RUNNING | 10.1.101.133 (eth0) |      | PERSISTENT | 0         |
+--------+---------+---------------------+------+------------+-----------+

$ for i in $(seq 1 6); do
  lxc file push --uid=0 --gid=0 --mode=0644 \
    /home/user/.ssh/id_rsa.pub \
    lxdhost:redis${i}/root/.ssh/authorized_keys
done
```

Now let's provision these hosts setting up empty unconfigured redis servers (you could just check [provision.yml from this repo](https://github.com/agrrh/ansible-redis-cluster/blob/master/provision.yml):

```
$ mkdir ansible-redis-cluster
$ cd ansible-redis-cluster

$ echo '[redis-cluster]' > inventory
$ lxc list -cn4 lxdhost: | grep -E redis[1-6] | awk '{print $2" ansible_host="$4}' >> inventory

$ ansible-playbook -i inventory provision.yml
```

Fun thing is that you should provide external IP as first bind address to prevent redis instances trying to connect neighbours via 127.0.0.1 as it uses first address by default. So correct form is: `bind ex.te.rn.al 127.0.0.1`.

If something went wrong and you need to start over, just reset hosts by issuing these 2 commands via ansible playbook:

```
tasks:
  - command: "redis-cli -h 127.0.0.1 -p {{ redis_port }} -a {{ redis_requirepass }} FLUSHALL"
  - command: "redis-cli -h 127.0.0.1 -p {{ redis_port }} -a {{ redis_requirepass }} CLUSTER RESET HARD"
  ...
```

Once you finished provisioning, you got 6 ready-to-meet password-protected redis servers. Let's build a cluster:

```
$ rcm create -a MyStronkPw \
  10.1.101.105:7001 \
  10.1.101.135:7002 \
  10.1.101.100:7003 \
  10.1.101.114:7004 \
  10.1.101.125:7005 \
  10.1.101.133:7006 \
  --masters 3
ADDSLOTS 0-5461 (total: 5462 slots)
OK
ADDSLOTS 5462-10923 (total: 5462 slots)
OK
ADDSLOTS 10924-16383 (total: 5460 slots)
OK
JOIN 6 nodes to 10.1.101.105:7001
OK
REPLICATE 10.1.101.100:7003
OK
REPLICATE 10.1.101.135:7002
OK
REPLICATE 10.1.101.105:7001
OK
```

And check it's status:

```
$ rcm schema -a MyStronkPw -h 10.1.101.105 -p 7001
[0-5461     ] 10.1.101.105:7001 10.1.101.133:7006
[5462-10923 ] 10.1.101.135:7002 10.1.101.125:7005
[10924-16383] 10.1.101.100:7003 10.1.101.114:7004

$ rcm status -a MyStronkPw -h 10.1.101.105 -p 7001
[0-5461     ] master(10.1.101.105:7001) with 1 slaves
[5462-10923 ] master(10.1.101.135:7002) with 1 slaves
[10924-16383] master(10.1.101.100:7003) with 1 slaves
```

In production environment with 3 physical hosts you probably would like to swap two of latest instances to distribute masters and slaves on different machines.

Now let's check it's writable:

```
# pip install redis-py-cluster
$ python
>>> from rediscluster import StrictRedisCluster
>>> startup_nodes = [{"host": "10.1.101.105", "port": "7001"}]
>>> rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True, password='MyStronkPw')
>>> rc.set("foo", "bar")
True
>>> rc.get("foo")
'bar'
```

Yep, it works as expected.
