Title: Nginx basic config examples
Date: 2015-07-17 10:58

Never better than [http://nginx.org/en/docs/](official nginx docs), but could be useful to rapidly deploy a webpage.

Return 444 when unknown domain asked:

    server {
        listen                  0.0.0.0:80 default;
        server_name             _;
        return                  444;
    }

Default server with static data:

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

Reverse proxy example:

    server {
        listen                  0.0.0.0:80;
        server_name             example.org www.example.org;

        set                     $PROXY_HOST 127.0.0.1;
        set                     $PROXY_PORT 81;

        location / {
            proxy_pass          http://$PROXY_HOST:$PROXY_PORT;
        }
    }

Example with php-fpm:

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
