Date: 2017-12-18 00:20
Category: Technical
Title: Minio, self-hosted S3-compatible storage
Tags: cloud, docker, minio, storage

Today I gonna tell you about great cloud-ready objects storage solution, [Minio](https://minio.io/).

To understand, what's a purpose of this software, one should know about Amazon's [Simple Storage Service](https://aws.amazon.com/s3) (which is S3). To be short, this is a storage and it stores objects. It's still possible to scale it and build tons of logic over the basic functionality, such as sending notifications when specific event occurs.

As a first step, we would deploy single-host storage instance from [Docker image](https://hub.docker.com/r/minio/minio/). Right now I'm using [Portainer](https://portainer.io/) to manipulate containers and it's super cool, but here I will show you generic command-line steps.

Let's create a container:

```
mkdir minio
docker run -d \
    --name minio \
    -p 9000:9000 \
    -v ${PWD}/minio/data:/data \
    -v ${PWD}/minio/conf:/root/.minio \
    minio/minio server /data
```

Well, we ran it in the background now, let's check an output to obtain secret and access keys, which were generated:

```
# docker logs minio
Created minio configuration file successfully at /root/.minio
Endpoint:  http://172.17.0.2:9000  http://127.0.0.1:9000
AccessKey: 5VJZMQJO0JDY19MJ9GQ2
SecretKey: A5tWRdLwULOX6+xsqGDm18te9m0BcOcnfANyt+Qq
...
```

Then we could visit [http://localhost:9000/](http://localhost:9000/) and see the UI:

![preview]({filename}/media/minio.png)

One could create a bucket (you've read about S3 terminology, right?) upload files and obtain share links here.

It's also possible to manipulate things with [command-line client](https://docs.minio.io/docs/minio-client-quickstart-guide). Yes, it is called `mc`, just like [midnight commander](https://midnight-commander.org/). :(

```
mc config host add myminio http://localhost:9000 5VJZMQJO0JDY19MJ9GQ2 A5tWRdLwULOX6+xsqGDm18te9m0BcOcnfANyt+Qq S3v4
mc ls myminio

# Create a bucket
mc mb myminio/test

# Upload a file and generate download link
mc copy some-file myminio/test/
mc share download myminio/test/some-file

# Cleanup
mc rm -r --force myminio/test
```

What else?

- You could scale it to provide high-availability with [docker swarm](https://docs.minio.io/docs/deploy-minio-on-docker-swarm) or [manually](https://docs.minio.io/docs/distributed-minio-quickstart-guide). [Kubernetes](https://docs.minio.io/docs/deploy-minio-on-kubernetes) is also an option.
- You could set up [notifications](https://docs.minio.io/docs/minio-bucket-notification-guide) to monitor objects activity.
- [Mirror valuable data](https://docs.minio.io/docs/store-mysql-backups-in-minio) from your hosts.
- Build a [backup system](https://docs.minio.io/docs/restic-with-minio) or [logs aggregation](https://docs.minio.io/docs/aggregate-apache-logs-with-fluentd-and-minio) over it.

Definitely, a great tool if you want to partially implement your own AWS for some reason.
