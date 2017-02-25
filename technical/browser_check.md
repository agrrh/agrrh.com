Title: Apache, User-Agent filtering
Date: 2015-07-17 11:27
Modified: 2017-02-25 13:31
Tags: apache, mod_rewrite
Summary: Фильтрация по User-Agent в Apache

Это была проверочная задача, кажется, в Яндексе.

Суть была в том, чтобы ограничить доступ к директории всем, кроме пользователей особого браузера: "Browser v3.14".

```plain
<Directory "/var/www">
  <IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteCond %{HTTP_USER_AGENT} !Browser\ v3\.14
    RewriteRule ^(.*)$ - [L,F]
  </IfModule>
</Directory>
```

Довольно просто.
