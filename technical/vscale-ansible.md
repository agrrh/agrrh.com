Title: Ansible for Vscale
Date: 2018-03-23 22:40
Tags: ansible, python, vscale

Today I would like to show you couple of useful scripts which let one manage [vscale.io](https://vscale.io) resources with Ansible.

[Dynamic Inventory](https://github.com/agrrh/ansible-vscale-inventory) - this tool let you forget about definitive inventory files. You just use this script which act as some kind of Ansible-to-provider-API proxy. Each time you run ansible, script goes to API and gathers actual data about your hosts.

[Modules](https://github.com/vscale/ansible-vscale-modules) - these scripts let you configure hosts right inside ansible code, like so:

```
- vscale_scalet:
    name: test
    state: started
```

Here's [my fork](https://github.com/agrrh/ansible-vscale-modules) with some fixes, official repo seems to be a little abandoned at the moment.
