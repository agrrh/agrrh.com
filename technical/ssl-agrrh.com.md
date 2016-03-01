Title: Free encryption for your own web page
Date: 2016-03-01 13:37

Hello!

I know 2 ways of getting free SSL certificate for your own web page.

Previously I was using StartSSL, it's free for a single domain usage:

<https://www.startssl.com/>

Now I moved to Let's Encrypt project:

<https://letsencrypt.org/>

And, of course, Nginx config is extra clean and friendly:

    server {
        listen                  your-ip-here:80;
        server_name             agrrh.com www.agrrh.com;
        rewrite ^(.*)           https://$server_name$1 permanent;
    }

    server {
        listen                  your-ip-here:443 ssl;
        ...
        ssl_certificate         /path/to/certificate/file;
        ssl_certificate_key     /path/to/private/key/file;
        ...
    }

Don't forget to restart and enjoy the green SSL sign in the address bar. :)
