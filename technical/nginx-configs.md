Title: Nginx basic config examples
Tags: nginx
Date: 2015-07-17 12:30
Modified: 2015-07-18 13:34

Never better than [official nginx docs](http://nginx.org/en/docs/), but could be useful to rapidly deploy a webpage.

### Return 444 when unknown domain asked:

    server {
        listen                  0.0.0.0:80 default;
        server_name             _;
        return                  444;
    }

### Default server with static data:

    server {
        listen                  0.0.0.0:80;
        server_name             example.org www.example.org;
        set                     $APP_ROOT /path/to/example.org;

        index                   index.html index.htm;
        autoindex               off;
        autoindex_exact_size    on;

        location / {
            root                $APP_ROOT;
        }
    }

### Reverse proxy example:

    server {
        listen                  0.0.0.0:80;
        server_name             example.org www.example.org;

        set                     $PROXY_HOST 127.0.0.1;
        set                     $PROXY_PORT 81;

        location / {
            proxy_pass          http://$PROXY_HOST:$PROXY_PORT;
        }
    }

### HTTP to HTTPS

    server {
        listen 10.0.0.1;
        server_name example.org www.example.org;
        rewrite ^ https://$server_name$request_uri? permanent;
    }
    server {
        server_name example.org www.example.org;
        listen 10.0.0.1:443 ssl;
        ssl on;
        ssl_certificate /var/www/httpd-cert/user/example.org.crt;
        ssl_certificate_key /var/www/httpd-cert/user/example.org.key;
        ...
    }

### Example with php-fpm:

    server {
        listen                  0.0.0.0:80;
        server_name             example.org www.example.org;
        set                     $APP_ROOT /path/to/example.org;

        index                   index.php index.html index.htm;
        autoindex               off;
        autoindex_exact_size    on;

        root                $APP_ROOT;

        location / {
            try_files          $uri $uri/index.html $uri.html @fallback =404;
        }

        location ~ \.php$ {
            root                $APP_ROOT;

            include             fastcgi_params;

            fastcgi_index       index.php;
            fastcgi_pass        unix:/var/run/php5-fpm.sock;
            # or using tcp address
            #fastcgi_pass        127.0.0.1:9000;
        }
    }

### Wordpress site example:

    upstream php {
            server unix:/var/run/php5-fpm.sock;
    }

    server {
        listen                  80 default_server;

        server_name             wp.agrrh.com www.wp.agrrh.com;

        set                     $APP_ROOT /var/www/agrrh/wordpress.agrrh.com;

        root                    $APP_ROOT;
        index                   index.php;

        location = /favicon.ico {
            log_not_found       off;
            access_log          off;
        }

        location = /robots.txt {
            allow               all;
            log_not_found       off;
            access_log          off;
        }

        location / {
            try_files           $uri $uri/ /index.php?$args;
        }

        location ~ \.php$ {
            #NOTE: You should have "cgi.fix_pathinfo = 0;" in php.ini
            include             fastcgi_params;
            fastcgi_intercept_errors on;
            fastcgi_pass        php;
        }

        location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
            expires             max;
            log_not_found       off;
        }
    }
