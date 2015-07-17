# connect
telnet mail.example.org 25

# HELO - domain from
HELO local.domain.com

# MAIL FROM
MAIL FROM: yourname@domain.com

# RCPT TO
RCPT TO: friend@otherdomain.com

# Message itself
DATA
SUBJECT: test
test
.

# done
QUIT