Date: 2018-09-26 15:44
Category: Technical
Title: Alertmanager, create silence via API
Tags: prometheus, jenkins

Sometimes your CI jobs execute heavy tasks which could lead to firing off some alerts. In this case it may be smart to automatically create short-lived silences to prevent such false-positive triggering.

It's possible to use default Prometheus Alertmanager's UI, but in this case we would like to automate, so here comes API.

We may do so via `POST /silences` call:

```
SILENCE_DATE_START=$(date +'%Y-%m-%dT%H:%M:%SZ')
SILENCE_DATE_END=$(date -d '+3 hour' +'%Y-%m-%dT%H:%M:%SZ')

cat > /tmp/alertmanager.json <<EOF
{
  "comment": "Example of silence created via Alertmanager API",
  "createdBy": "CI/CD system job",
  "startsAt": "${SILENCE_DATE_START}",
  "endsAt": "${SILENCE_DATE_END}",
  "matchers": [
    {"isRegex": false, "name": "job", "value": "my-instance"},
    {"isRegex": false, "name": "project", "value": "some-more-selectors"},
    {"isRegex": true, "name": "mountpoint", "value": "/(root|home/*)"}
  ]
}
EOF

curl --data '@/tmp/alertmanager.json' http://alertmanager.example.org/api/v1/silences
```

You're free to POST it via `curl` or any other utility (consider take a look at `httpie`):

And, of course, you could also use `amtool`:

```
$ amtool silence add job="my-instance" project="some-more-selectors" "mountpoint"=~"/(root|home/*)"
e48cb58a-0b17-49ba-b734-3585139b1d25

$ amtool silence expire e48cb58a-0b17-49ba-b734-3585139b1d25
```

See more examples here: https://github.com/prometheus/alertmanager/blob/master/README.md#amtool
