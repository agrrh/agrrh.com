Date: 2018-11-03 23:50
Category: Technical
Title: RunC vs Kata containers performance
Tags: docker, runc, kata

Basically, Docker uses RunC to provide lightweight and isolated environment for your software.

Since whole Docker nowadays consists of extensible Moby project, one could implement their own environment and run "containers" with other technologies, for example, pure `exec` or `qemu`. In last case you porbably mean [Kata Containers](https://katacontainers.io/) project, same containers, but actually virtual machines.

So I was using two 5$ hosts on [DigitalOcean](https://m.do.co/c/296358d8a9d3) to test how much overhead Kata adds to my services. One to run container, one to generate workload over internal network.

Here's a simple gist on how to [install Docker CE with Kata](https://gist.github.com/agrrh/f9a55ef5c2aed4178ca6a9f7b542f282) on Ubuntu server.

Then you would like to run simple service to compare performance, I was using my [dummy-service-py](https://hub.docker.com/r/agrrh/dummy-service-py/), feel free to use it too.

Results are following:

| 🐳          | RunC | Kata |
|-
|Workload     | `siege -c 512 -t 60s` | `siege -c 512 -t 60s` |
|Availability | 100% | 100% |
|Transactions | 43274 hits | 17548 hits |
|Response time| 0.20 s | 1.17 s |
|Rate         | 724.37 trans/sec | 293.05 trans/sec |
|Concurrency  | 145.08 | 342.96 |
|**Resources:**|||
|CPU usage    | ~100%| ~100% |
|Memory usage | ~20M | ~150M |

It's safe to say we can see top performance of RunC container here while Kata container (VM) was a little bit oveloaded so performance degraded. If we drop concurrency down, the gap between those technologies wouldn't be so huge, but still very significant.

Kata containers look like an interesting tool to limit resources between containers in a "hard" way, for example.

Whole idea is still ironic: containers came to evade VM overhead and provide lightweight isolation, so here's VMs for your containers engine, just in case. :)
