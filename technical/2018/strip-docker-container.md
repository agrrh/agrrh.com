Title: Strip Docker container
Date: 2018-02-17 07:15
Tags: docker, bash

Today we would get rid of all unnecessary stuff in our Docker images.

To be honest, this task is not really useful in real life due to layered filesystem Docker uses. So even in case of huge images, you store base only once. Then it's all about relatively small deltas.

Only sane reason which I'm able to imagine is security: let's say we don't want to simplify hackers life by providing system utilities. :) But another side is that we also make our IT guys life a little bit of hell. They would be almost unable to investigate issues on running containers.

Anyways, here's how you make things done:

### Prepare source image

Hello-world Node.JS app in my case:

```
# Dockerfile
FROM node:8-alpine
RUN apk update && apk add bash  # We must add bash to let magic happen
WORKDIR /app
COPY ./main.js /app/main.js
CMD ["node", "/app/main.js"]
```

Then I just `docker build` it tagged as `my-nodejs-app`.

### Strip the image

This is when I need some additional tool: [strip-docker-image](https://github.com/agrrh/strip-docker-image).

Here I use my own fork as original application doesn't support Alpine at the moment. **Update:** now it does, author [merged it in](https://github.com/mvanholsteijn/strip-docker-image/commit/2bec01f2718e741a1b7fceb39ba3c1a21613e402).

```
git clone https://github.com/agrrh/strip-docker-image
cd strip-docker-image

./bin/strip-docker-image -v \
    -i my-nodejs-app:latest \
    -t my-nodejs-app:stripped \
    -f /usr/local/bin/node \
    -f /app/main.js
```

Let's see if it works:

```
$ docker run -ti my-nodejs-app:stripped
Server running at http://0.0.0.0:8081/
```

### We need to go deeper

If we're able to run something but our app?

```
$ docker run -ti my-nodejs-app:latest ls
main.js

$ docker run -ti my-nodejs-app:stripped ls
docker: Error response from daemon: OCI runtime create failed: container_linux.go:296: starting container process caused "exec: \"ls\": executable file not found in $PATH": unknown.
```

Great. Just what we needed.

But how much space did we saved?

```
my-nodejs-app             latest              528c21f4392a        About an hour ago   72.7MB
my-nodejs-app             stripped            1a09fb91336e        About an hour ago   38.7MB
```

Sadly, not too much.

Let's see how it looks from inside:

```
$ docker image save my-nodejs-app:stripped -o tmp.tar
$ tar xvf tmp.tar
$ tar tf <layer-id>/layer.tar
app/
app/main.js
lib/
lib/ld-musl-x86_64.so.1
usr/
usr/lib/
usr/lib/libgcc_s.so.1
usr/lib/libstdc++.so.6
usr/lib/libstdc++.so.6.0.22
usr/local/
usr/local/bin/
usr/local/bin/node
```

And that's all content of our fully-functional containerized app.

Seems fun, but remember not to be penny wise and pound foolish.
