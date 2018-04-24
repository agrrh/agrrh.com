Date: 2018-04-12 12:02
Category: Technical
Title: Jinja2: lstrip_blocks to manage indentation
Tags: ansible, jinja

This post is a mirror of [ansiblemaster.wordpress.com/jinja2-lstrip_blocks-to-manage-indentation](https://ansiblemaster.wordpress.com/2016/07/29/jinja2-lstrip_blocks-to-manage-indentation/) and saved here to prevent it's abyssal by void.

According to [Jinja2 documentation](http://jinja.pocoo.org/docs/dev/templates/#whitespace-control) you can manage whitespace and tabular indentation with lstrip_blocks and trim_blocks options:

trim_blocks: If this is set to True the first newline after a block is removed (block, not variable tag!). Defaults to False.
lstrip_blocks: If this is set to True leading spaces and tabs are stripped from the start of a line to a block. Defaults to False.
By default Ansible templates have trim_blocks true and lstrip_blocks false. If you want to manage them you can do it if you set them at the very beginning of your template file as follows:

```
#jinja2: lstrip_blocks: "True (or False)", trim_blocks: "True (or False)"
```

So, if you have following Ansible code for /etc/hosts template:

```
{% for host in groups['webservers'] %}
    {% if inventory_hostname in hostvars[host]['ansible_fqdn'] %}
{{ hostvars[host]['ansible_default_ipv4']['address'] }} {{ hostvars[host]['ansible_fqdn'] }} {{ hostvars[host]['inventory_hostname'] }} MYSELF
    {% else %}
{{ hostvars[host]['ansible_default_ipv4']['address'] }} {{ hostvars[host]['ansible_fqdn'] }} jcs-server{{ loop.index }} {{ hostvars[host]['inventory_hostname'] }}
    {% endif %}
{% endfor %}
```

By default Ansible will indent as you’re doing in your code:

```
     192.168.1.2 web01
               192.168.1.3 web02
               192.168.1.4 web03
```

But if you add at the top of your template the following code:

```
#jinja2: lstrip_blocks: "True"
```

Result will be without indentation:

```
192.168.1.2 web01
192.168.1.3 web02
192.168.1.4 web03
```

That makes you able to write more readable jinja2 code in your templates.

Please, note that you can’t delete indentation of the code that will be written in your final file. So in our case we’ve defined hostvars variables at the very beginning of our line because we wanted them there. If you indent that code, your result will be indented.
