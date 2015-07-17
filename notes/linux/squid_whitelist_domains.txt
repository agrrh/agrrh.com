# squid.conf
auth_param digest program /usr/lib/squid3/digest_pw_auth -c /etc/squid3/passwords
auth_param digest realm proxy
acl authenticated proxy_auth REQUIRED

# create a password
htdigest -c /etc/squid3/passwords proxy user

# squid.conf again
acl whitelist dstdomain "/etc/squid3/white.list"
http_access allow whitelist authenticated
