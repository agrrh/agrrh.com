Title: From Jenkins to Teamcity
Date: 2017-09-29 00:14
Tags: jenkins, teamcity, cicd

Earlier I told that my [Jenkins was hacked](/2017/my-jenkins-was-hacked). Not sure how, but it's current Docker image is definitely vulnerable.

So I moved to TeamCity, it looked great to me since 2014 when I was working at Yandex as Linux SA.

Running server (UI and project manage data) container:

```
# Path to local dir to make config persistent between different containers
#   This must be absolute path, otherwise docker fails to bind volume
LOCAL_DATA_DIR=/opt/docker_data/

# Port to expose teamcity UI on local address
TEAMCITY_PORT=8111

docker run -d --name teamcity-server --restart=always \
  -v ${LOCAL_DATA_DIR}/teamcity-server/data:/data/teamcity_server/datadir \
  -v ${LOCAL_DATA_DIR}/teamcity-server/logs:/opt/teamcity/logs \
  -p ${TEAMCITY_PORT}:8111 \
  jetbrains/teamcity-server
```

Then we need agents (almost same as Jenkins agents or GitLab runners), at lease one:

```
# IP of docker bridge to connect agents to head host even with zero knowledge of particular container's address
#   This is default one
DOCKER_BRIDGE_IP=172.17.0.1

# Same values
LOCAL_DATA_DIR=/opt/docker_data/
TEAMCITY_PORT=8111

for i in 1; do
  docker run -d --name teamcity-agent${i} --restart=always \
    -e SERVER_URL="http://${DOCKER_BRIDGE_IP}:8111/" \
    -v ${LOCAL_DATA_DIR}/teamcity-agent${i}:/data/teamcity_agent/conf \
    jetbrains/teamcity-agent
done
```

And making it available from outer world, here's an example for great [Caddy](https://caddyserver.com/) server:

```
# /etc/caddy/Caddyfile

import ./conf.d/*.conf

# /etc/caddy/conf.d/teamcity.example.org.conf

teamcity.example.org {
  proxy / 127.0.0.1:8111 {
    transparent
  }

  basicauth / login password
  # or use ipfilter here

  log /var/log/caddy/teamcity.example.org.access.log {
    rotate_size 100
    rotate_age 7
    rotate_keep 10
  }
  errors /var/log/caddy/teamcity.example.org.errors.log {
    rotate_size 100
    rotate_age  7
    rotate_keep 10
  }
}
```

Voila, it was easy as one-two-three. Proceed to defining new projects and keep in mind that you got only 20 free builds, then it asks for money. :)
