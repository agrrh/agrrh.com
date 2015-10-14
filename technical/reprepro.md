Title: Deploy of deb repository with reprepro
Tags: deb, reprepro
Date: 2015-10-14 12:10

This article represents instruction on setup debian repository with reprepro. Very basic, but still useful.

Host setup:

    # as 'root' user
 
    apt-get update
    apt-get install dpkg-sig reprepro nginx
 
    vim /etc/nginx/sites-available/repo.conf # see contents below
 
    ln -s /etc/nginx/sites-available/repo.conf /etc/nginx/sites-enabled/repo.conf
    nginx -t
 
    adduser repo
    su - repo
 
    # as 'repo' user
 
    mkdir -p repo/conf
    cd $_
 
    gpg --gen-key
    gpg --armor --output ~/repo/repo_wheezy.pub.gpg.key --export "Repo Wheezy"
 
    vim distributions # see contents below
    vim options # see contents below
 
    reprepro includedeb wheezy /path/to/package.deb
    reprepro export
 
    # as 'root' user again
 
    service nginx restart

Example of `conf/distributions`:

    Origin: Debian
    Label: Wheezy apt repository
    Codename: wheezy
    Architectures: amd64
    Components: main
    Description: Apt repository for Debian stable - Wheezy
    SignWith: CHANGEME # change to actual value, see with 'gpg --list-keys'

Example of `conf/options`:

    verbose
    basedir /home/repo/repo
    ask-passphrase

Example of simple nginx directory listing via http:

    server {
      listen 80 default_server;
    
      root /home/repo;
 
      #  index index.html index.htm;
 
      server_name my-repo-address;
 
      location / {
        autoindex on;
        autoindex_exact_size off;
      }
    }

Usage examples:

    # as 'repo' user
    
    # always work from repo's base directory
    cd ~/repo
    
    # include single deb package
    reprepro includedeb wheezy /path/to/package.deb
    reprepro export
 
    # remove single deb file
    reprepro remove wheezy PACKAGE_NAME
    reprepro export

Client configuration:

    # as 'root' user
     
    wget http://my-repo-address/repo/repo_wheezy.pub.gpg.key
    apt-key add repo_wheezy.pub.gpg.key
 
    echo "deb [arch=amd64] http://my-repo-address/repo wheezy main" >> /etc/apt/sources.list.d/my-repo.list
    apt-get update
 
    apt-cache policy PACKAGE_NAME
