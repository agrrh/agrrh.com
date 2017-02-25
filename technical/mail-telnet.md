Title: Email via telnet
Date: 2015-07-17 12:38
Tags: telnet, mail

Here's a brief recipe on how to send email with just a bare telnet.

Establish a connection with mail server:

    telnet mail.example.org 25

Introduce yourself:

    HELO local.domain.com
    MAIL FROM: yourname@domain.com

And tell who is the recipient:

    RCPT TO: friend@otherdomain.com

Now form a message itself (last dot commits message end):

    DATA
    SUBJECT: test
    test
    .

That's it. :)

    QUIT
