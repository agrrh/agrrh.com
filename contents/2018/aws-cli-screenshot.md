Date: 2018-08-27 14:09
Category: Technical
Title: AWS EC2 instance screenshot
Tags: aws, ec2, shortcut

Sometimes you would like to know what happens with your EC2. Especially when it's unreachable and failed to start logging daemon. Despite absence of IP-KVM, you still may access your instance screen with `aws` CLI tool:

```
aws ec2 get-console-screenshot --instance-id i-0e434bded75493e2d | jq -cr '.ImageData' | base64 --decode > tmp.jpg
```

This command will create screenshot and save it to `tmp.jpg` in your local folder.

Of course, you need to set `AWS_*` env vars: https://docs.aws.amazon.com/cli/latest/userguide/cli-environment.html
