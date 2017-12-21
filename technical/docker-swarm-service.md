Date: 2017-12-21 21:17
Title: Scale microservice with Docker Swarm
Tags: docker, swarm, python

At first, this article is VERY similar to this one from [Alex Ellis](https://blog.alexellis.io/microservice-swarm-mode/) blog and differs only with some insignificant details. Feel free to follow the link and read original one.

Here I would:

- Bring up Docker in swarm mode using single node
- Deploy a simple service with replication factor of 5

We would also learn how to rebalance containers over nodes after adding one more node to our setup.

### Bringing up Docker in swarm mode

Assuming you're working with root-level privelege, let's make sure you got docker installed:

```
apt update
apt upgrade -y
apt install docker.io -y
```

Then initialize swarm mode would be as simple as:

```
docker swarm init
```

### Create a new service

```
# docker service create --name dummy --publish 9005:9005 agrrh/dummy-service-py
```

Voila, we created a new service with port 9005 exposed to real world and available at this node's external IP.

After a couple of moments service becomes available:

```
# docker service ls
ID            NAME   MODE        REPLICAS  IMAGE
yo997oy1qdaj  dummy  replicated  1/1       agrrh/dummy-service-py:latest
```

Let's now check how it works:

```
# wget -q -O - http://external-ip:9005/
{
  "hostname": "2ff9d0643888",
  "uuid": "d40cb486-f460-4520-9c2c-7f0b2c9ad072"
}

# wget -q -O - http://external-ip:9005/
{
  "hostname": "2ff9d0643888",
  "uuid": "d50cb90a-cab2-400c-8b95-30ecbb1490a7"
}
```

Yes, we got different UUIDs with each request.

### Rescale service to 5 instances

```
# docker service scale dummy=5

# docker service ls
ID            NAME   MODE        REPLICAS  IMAGE
zig7hmjz3sd8  dummy  replicated  5/5       agrrh/dummy-service-py:latest
```

How would it work now?

```
# wget -q -O - http://external-ip:9005/
{
  "hostname": "ec6a4f86a0ae",
  "uuid": "f96b1435-fc01-4eb5-b4f0-f272eef413d7"
}
# wget -q -O - http://external-ip:9005/
{
  "hostname": "20fd2dd80ef0",
  "uuid": "e8482d91-fbff-43d1-ab4c-6d6c68278183"
}
# wget -q -O - http://external-ip:9005/
{
  "hostname": "adc64013e44f",
  "uuid": "86e8b384-1f45-49bd-b74a-e9a887f43059"
}
```

Okay, but it still uses single node and this is a huge availability risk, let's distribute it over the data-center.

### Add 2nd node and rebalance containers

On the second (and all other new nodes) we would like to join the swarm as worker:

```
# On original manager
# docker swarm join-token worker

# On new worker
# docker swarm join \
    --token <very-long-token-here> \
    <external-ip>:2377
```

Swarm uses port 2377 for cluster management communications.

Nodes should also see each other via 7946/tcp, 7946/udp and 4789/udp ports. See details in [official docs](https://docs.docker.com/engine/swarm/swarm-tutorial/#open-protocols-and-ports-between-the-hosts).

After 2nd node joined cluster, it is completely empty, but we would force service redistribution:

```
# On new worker
# docker ps -q | wc -l
0

# On the manager node
# docker service update --force dummy
```

Then you wait for a couple of moments and voila:

```
ID            NAME     IMAGE                          NODE            DESIRED STATE  CURRENT STATE           ERROR  PORTS
yvdyg8x9xg2s  dummy.1  agrrh/dummy-service-py:latest  docker-worker1  Running        Running 22 seconds ago         
r8ctq0y7g9w9  dummy.2  agrrh/dummy-service-py:latest  docker-manager  Running        Running 18 seconds ago         
k1l36hivwg02  dummy.3  agrrh/dummy-service-py:latest  docker-manager  Running        Running 14 seconds ago         
0afl0qbye00q  dummy.4  agrrh/dummy-service-py:latest  docker-worker1  Running        Running 10 seconds ago         
385zd2fuhjk3  dummy.5  agrrh/dummy-service-py:latest  docker-manager  Running        Running 6 seconds ago
```

How it works now?

```
# wget -q -O - http://external-ip:9005/
{
  "hostname": "yvdyg8x9xg2s",
  "uuid": "167d645c-c2ab-479f-a002-abd9a9dba968"
}
# wget -q -O - http://external-ip:9005/
{
  "hostname": "r8ctq0y7g9w9",
  "uuid": "be135c86-62bd-4e99-b5a2-9742eec247e9"
}
# wget -q -O - http://external-ip:9005/
{
  "hostname": "k1l36hivwg02",
  "uuid": "cf742aba-e6d4-4c3d-960d-21a7377b9d80"
}
```

As you see, we can reach containers on different nodes via same IP-address and port number pair.

Kind of magic, eh?

# Cleanup

After it's done, we probably would like to remove our test setup gracefully:

```
# On worker node
# docker swarm leave

# On manager node
# docker swarm leave --force
```
