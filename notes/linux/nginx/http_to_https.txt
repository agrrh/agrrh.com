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