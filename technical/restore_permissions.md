Title: How to restore permissions on Debian system
Date: 2015-08-01 21:29
Tags: permissions, restore, how to

This gonna be a simple recipe on file permissions restore in Debian system. I was using same recipe while working at [FastVPS](http://fastvps.ru/) as Tech Support. It's very useful after occasional `chown -Rf user: /` or `chmod -Rf 777 /`. Both occurs frequently than you could think.

### First way: Donor system

Save packages list from corrupted system while it still works to the file:

    # with exact versions
    PKGS=$(dpkg -l | grep ^ii | awk '{print $2" "$3}' | tr ' ' '=')

    # just package names with specified arch
    PKGS=$(dpkg --get-selections | grep -v 'deinstall' | awk '{print $1}')

    echo $PKGS > /tmp/packages_to_install.list

Afterwards you should just install these packages on donor system and save correct permissions (don't forget to use same repos):

    # installing packages
    PKGS=$(cat ~/packages_to_install.list)
    apt-get install $PKGS

    # saving permissions mask
    find / -exec stat --format "chmod %a %n" {} \; > /tmp/restore_perms.sh
    find / -exec stat --format "chown %U:%G %n" {} \; >> /tmp/restore_perms.sh

And then just transfer script to the corrupted system and run it:

    bash /tmp/restore_perms.sh

Now it's time to pray and restart services / reboot the system. That's it. :)

### Second way: use info from *.deb files

Just use following script:

    #!/bin/bash
    # Restores file permissions for all files on a debian system for which .deb
    # packages exist.
    #
    # Author: Larry Kagan <me at larrykagan dot com>
    # Modified: Kirill Kovalev / http://agrrh.com/
    # Since 2007-02-20

    ARCHIVE_DIR=/var/cache/apt/archives/
    PACKAGES=$(ls $ARCHIVE_DIR)

    cd /

    function changePerms() {
        CHOWN="/bin/chown"
        CHMOD="/bin/chmod"
        #PERMS=$1
        PERMS=`echo $1 | sed -e 's/--x/1/g' -e 's/-w-/2/g' -e 's/-wx/3/g' -e 's/r--/4/g' -e 's/r-x/5/g' -e 's/rw-/6/g' -e 's/rwx/7/g' -e 's/---/0/g'`
        PERMS=`echo ${PERMS:1}`
        OWN=`echo $2 | /usr/bin/tr '/' '.'`
        PATHNAME=$3
        PATHNAME=`echo ${PATHNAME:1}`
        echo -e "CHOWN: $CHOWN $OWN $PATHNAME"
        result=`$CHOWN $OWN $PATHNAME`

        if [ $? -ne 0 ]; then
            echo -e $result
        fi

        echo -e "CHMOD: $CHMOD $PERMS $PATHNAME"
        result=`$CHMOD $PERMS $PATHNAME`

        if [ $? -ne 0 ]; then
            echo -e $result
        fi
    }

    for PACKAGE in $PACKAGES; do
        if [ -d $PACKAGE ]; then
            continue;
        fi

        echo -e "Getting information for $PACKAGE\n"
        FILES=$(/usr/bin/dpkg -c "${ARCHIVE_DIR}${PACKAGE}")
        for FILE in "$FILES"; do
            #FILE_DETAILS=`echo "$FILE" | awk '{print $1"\t"$2"\t"$6}'`

            echo "$FILE" | awk '{print $1"\t"$2"\t"$6}' | while read line; do
                changePerms $line
            done
            #changePerms $FILE_DETAILS
        done
    done

Also same result could be achieved with a script:

    #!/bin/bash
    for pkg in `dpkg --get-selections | egrep -v deinstall | awk '{print $1}' | egrep -v '(dpkg|apt|mysql|mythtv)'` ; do apt-get -y install --reinstall $pkg ; done

Idea and second way scripts were copied from [this blog](http://sysadminnotebook.blogspot.ru/2012/06/how-to-reset-folder-permissions-to.html).
