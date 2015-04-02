We assume SSL is already present for domain

Check SSL
[http://www.sslshopper.com/ssl-checker.html]

Fetch the Root CA and Class 1 Intermediate Server CA certificates:
```
wget http://www.startssl.com/certs/ca.pem
wget http://www.startssl.com/certs/sub.class1.server.ca.pem
```

Create a unified certificate from your certificate and the CA certificates:

```
cat ssl.crt sub.class1.server.ca.pem ca.pem > /etc/nginx/conf/ssl-unified.crt
```

Configure your nginx server to use the new key and certificate (in the global settings or a server section):

```
ssl on;
ssl_certificate /etc/nginx/conf/ssl-unified.crt;
ssl_certificate_key /etc/nginx/conf/ssl.key;
```
