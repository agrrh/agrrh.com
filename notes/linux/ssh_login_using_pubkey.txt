# on client
ssh-keygen -t rsa
cat .ssh/id_rsa.pub

# on host
echo "CLIENT_PUB_KEY" >> .ssh/authorized_keys2

# afterwards on client again
# authorization works automatically
ssh 1.2.3.4

# OR JUST

ssh-copy-id user@target