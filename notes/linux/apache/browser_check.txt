<Directory "/var/www/mywebsql">
  <IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteCond %{HTTP_USER_AGENT} !Browser\ v3\.14
    RewriteRule ^(.*)$ - [L,F]
  </IfModule>
</Directory>