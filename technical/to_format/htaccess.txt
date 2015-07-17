# close this site
Order Deny,Allow
Deny from all

# allow everything here
Order Allow, Deny
Allow from all

# for specific file
<Files "index.php">
Order Deny,Allow
Deny from all
</Files>

# close for specific host
Order Allow,Deny
Allow from all
Deny from 12.34.56.78
Deny from 12.34.56
Deny from site.ru

# close number of files
<Files "\.(sql|phps)$">
Order Allow,Deny
Deny from all
</Files>

# redirects
Redirect / http://www.example.com

# non-www -> www
RewriteCond %{HTTP_HOST} !^www\.
RewriteRule ^(.*)$ http://www.%{HTTP_HOST}/$1 [R=301,L]

# www -> non-www
RewriteCond %{HTTP_HOST} ^www. [NC]
RewriteRule ^(.*)$ http://my-domain.com/$1 [R=301,L]

# http to https
RewriteEngine On
RewriteCond %{HTTPS} !=on
RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [R,L]

# trailing slash
RewriteCond %{REQUEST_URI} !\.[^./]+$
RewriteCond %{REQUEST_URI} !(.*)/$
RewriteRule ^(.*)$ http://my-domain.com/$1/ [R=301,L]

# remove index.php from url
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /index.php?/$1 [L]
