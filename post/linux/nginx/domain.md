server {
#    listen                  80 default_server;
    listen                  80;

    server_name             example.org www.example.org;

    set                     $PROXY_HOST 127.0.0.1;
    set                     $PROXY_PORT 81;
    include                 /etc/nginx/proxy_params;

    set                     $APP_ROOT /path/to/example.org;

    index                   index.php index.html index.htm;
#    autoindex               off;
#    autoindex_exact_size    on;

    location / {
        root                $APP_ROOT;
    }

#    location / {
#        try_files          $uri $uri/index.html $uri.html @fallback =404;
#    }

#    location @fallback {
#        proxy_pass         http://$PROXY_HOST:$PROXY_PORT;
#    }

    location ~* .(jpg|jpeg|gif|png|ico|css|bmp|swf|js|mov|avi|mp4|mpeg4|tar.gz|tar) {
        root                $APP_ROOT;
    }

    location ~ \.php$ {
        proxy_pass            http://$PROXY_HOST:$PROXY_PORT;
    }



    location ~ \.php$ {
        root                $APP_ROOT;

        include             fastcgi_params;

        fastcgi_index       index.php;
        fastcgi_pass        unix:/var/run/php5-fpm.sock;
#        fastcgi_pass        127.0.0.1:9000;
    }

    location ~ /.ht {
        deny                all;
    }
}