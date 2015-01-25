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