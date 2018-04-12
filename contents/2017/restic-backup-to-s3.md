Date: 2017-12-20 16:23
Category: Technical
Title: Organize backups with Restic and S3
Tags: restic, docker, backups, aws, minio

Few days ago we set up [Minio](/2017/minio-self-hosted-s3-compatible-storage), AWS S3-compatible storage.

Let's now use another awesome utility, [Restic](https://restic.github.io/), to make backups with snapshots and rotation.

In this example I would be using S3 storage based on `minio`, but it's okay to use AWS one or just a local folder. Another particularity is that I use docker image, but it's almost the same as if I use restic installed locally.

By the way, Amazon offers [free S3 tier](https://aws.amazon.com/s3) with up to 5GB storage and 15GB of monthly traffic and 2k/20k of PUT/GET requests.

First, I'm starting the restic container. You could obtain keys from Minio UI or by checking related contanier's logs:

```
docker logs minio

# Here I use "v1.0" tag due to "latest" image is experimental non-stable version
# Check repository in order to make sure which version is the latest stable.
# Also there you could read about available env variables.
#   https://hub.docker.com/r/lobaro/restic-backup-docker/

docker run -d --name restic \
  -e "RESTIC_REPOSITORY=s3:http://minio-external-ip:9000/backups/" \
  -e "AWS_ACCESS_KEY_ID=3ADAE8O8YVS726UA4BZM" \
  -e "AWS_SECRET_ACCESS_KEY=KbJtZPoVvGbXsaD2LsxvJZF/7LRi4FhT0TK4gDQq" \
  -e "RESTIC_PASSWORD=ThisRepoPassword" \
  -v /mnt/my-sensitive-data-dir:/data:ro \
  lobaro/restic-backup-docker:v1.0
```

Then, let's check restic logs to make sure there're no errors:

```
$ docker logs restic
Starting container ...
Restic repository 's3:http://minio-external-ip:9000/backups/' does not exists. Running restic init.
Setup backup cron job with cron expression BACKUP_CRON: * */6 * * *
Container started.
```

Here we could see that by default there is a backup cron job that saves data every 6 hours. Let's perform first save manually:

```
$ docker exec -ti restic backup
Starting Backup
Backup Successfull
```

After number of automated saves we could see following stored snapshots:

```
$ docker exec -ti restic restic snapshots
ID        Date                 Host        Tags        Directory
----------------------------------------------------------------------
ea76d151  2017-12-20 13:05:42  restic                  /data
558f01ec  2017-12-20 14:00:02  restic                  /data
fe749981  2017-12-20 15:00:02  restic                  /data
9b2a6216  2017-12-20 16:00:02  restic                  /data
```

We've could restore one of the snapshots but in this very example I set up read-only volume in order to not accidentally corrupt data, so just in case you interested this is as simple as:

```
docker exec -ti restic restic restore <snapshot_id>
```

Well, we're done with a great automated backups. You could further customize it with cleanup policies and automated rotation by [reading this documentation section](https://restic.readthedocs.io/en/stable/060_forget.html#removing-snapshots-according-to-a-policy).
