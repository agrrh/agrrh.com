Title: mod_rewrite and User-agent
Date: 2015-07-17 11:27
Category: notes
Tags: apache, mod_rewrite
Authors: Kirill Kovalev
Summary: Rewrite rule that restricts access, based on User-agent

This was an exam task somewhere.

The case is to restrict access to the directory for everyone except specific browser users. "Browser v3.14" in that example.

    <Directory "/var/www">
      <IfModule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{HTTP_USER_AGENT} !Browser\ v3\.14
        RewriteRule ^(.*)$ - [L,F]
      </IfModule>
    </Directory>

Easily done.
