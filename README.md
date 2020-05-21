# Ansible Locate (for Collection Content)

This is a tool which will walk around the YAML files in your playbook project
and then suggest where to get that content from collections.

```
ansible-locate install.yml
```

Will just print stuff. This may give you enough information to
`ansible-galaxy collection install` the collections needed for the `install.yml`
playbook to run. That comes with a few qualifiers about pathing issues.

Having the collections alone is not enough, you also need to change the
task names. In the narrow case of roles, there is another option to add
a meta/routing.yml file to point to the new location.

This tool will fill those in by doing:

```
ansible-locate install.yml --write-meta
```

Adding routing stuff will become a little obsolete if the general
tombstoning and routing pull request is merged. However, it _can_ still
help to have so that Ansible 2.9 will pull content from your collections.
Also, there is still the problem of knowing _what_ to install for
legacy Ansible stuff, which this can still be useful for.

#### Demo

This is not a great example, but it's a public repo...

```
$ ansible-locate ~/Documents/repos/jlaska-ansible-playbooks/
Locked and loaded with 3752 module redirects

Inspecting playbooks
 skipping playbook /Users/alancoding/Documents/repos/jlaska-ansible-playbooks/custom_json_vars.yml
 skipping playbook /Users/alancoding/Documents/repos/jlaska-ansible-playbooks/vaulted_debug_hostvars.yml
  playbook /Users/alancoding/Documents/repos/jlaska-ansible-playbooks/async_tasks.yml
    async_status --> ansible.windows.async_status
 skipping playbook /Users/alancoding/Documents/repos/jlaska-ansible-playbooks/vault.yml
 skipping playbook /Users/alancoding/Documents/repos/jlaska-ansible-playbooks/vaulted_ansible_env.yml
  playbook /Users/alancoding/Documents/repos/jlaska-ansible-playbooks/tower_collection_smoke.yml
    tower_job_launch --> awx.awx.tower_job_launch
    tower_job_list --> awx.awx.tower_job_list

Inspecting role directories

Overall routing:
---
async_status: ansible.windows.async_status
tower_job_launch: awx.awx.tower_job_launch
tower_job_list: awx.awx.tower_job_list


The collections/requirements.yml file you would need:
---
collections:
  - awx.awx
  - ansible.windows
```

Another public example:

```
$ ansible-locate ~/Documents/repos/utility-playbooks/
Locked and loaded with 3752 module redirects

Inspecting playbooks
  playbook /Users/alancoding/Documents/repos/utility-playbooks/tower_module.yml
    tower_organization --> awx.awx.tower_organization
 skipping playbook /Users/alancoding/Documents/repos/utility-playbooks/contradict.yaml
  playbook /Users/alancoding/Documents/repos/utility-playbooks/cloud_module_testing.yml
    ec2 --> amazon.aws.ec2
    os_server --> openstack.cloud.os_server
    vmware_guest --> community.vmware.vmware_guest
    ovirt_auth --> ovirt.ovirt.ovirt_auth
    tower_inventory --> awx.awx.tower_inventory
  playbook /Users/alancoding/Documents/repos/utility-playbooks/gce_lookup.yaml
    gcp_compute_disk --> google.cloud.gcp_compute_disk
  playbook /Users/alancoding/Documents/repos/utility-playbooks/tower_module_chris.yml
    tower_organization --> awx.awx.tower_organization
  playbook /Users/alancoding/Documents/repos/utility-playbooks/tower_module_ct.yml
    tower_credential_type --> awx.awx.tower_credential_type

Inspecting role directories
  roles/awx-collection-publisher/tasks/main.yml
    tower_organization --> awx.awx.tower_organization
    tower_project --> awx.awx.tower_project
    tower_inventory --> awx.awx.tower_inventory
    tower_host --> awx.awx.tower_host
    tower_credential_type --> awx.awx.tower_credential_type
    tower_job_template --> awx.awx.tower_job_template

Overall routing:
---
ec2: amazon.aws.ec2
gcp_compute_disk: google.cloud.gcp_compute_disk
os_server: openstack.cloud.os_server
ovirt_auth: ovirt.ovirt.ovirt_auth
tower_credential_type: awx.awx.tower_credential_type
tower_host: awx.awx.tower_host
tower_inventory: awx.awx.tower_inventory
tower_job_template: awx.awx.tower_job_template
tower_organization: awx.awx.tower_organization
tower_project: awx.awx.tower_project
vmware_guest: community.vmware.vmware_guest


The collections/requirements.yml file you would need:
---
collections:
  - openstack.cloud
  - awx.awx
  - community.vmware
  - ovirt.ovirt
  - amazon.aws
  - google.cloud
```

#### Pathing Behavior

This is intended to be _project based_ not _runtime based_.

You might put roles into all kinds of places on your computer, and then
add them to search paths by `ansible.cfg`, environment variables, or heck,
even collections.

This tool will not follow those. It just looks in the `roles` directory
relative to the location it was given.

#### Known Issues

If you use the `slurp` module, this tool will think it belongs in the
windows collection. It does not. From IRC:

> slurp is 'special case' and probably should be removed from routing,
> some windows modules are 'attached' to their posix counterparts, slurp, fetch, setup ...

So this is left broken for now, anticipating further churn.
You may need to manually remove these entries.

### Similar things

Lookup FQCN of plugins from Playbooks or task files, and print their FQCN from routing.yml
https://gist.github.com/sivel/73a071faa7b37a851437a026aa94f7da

Script to rewrite an Ansible playbook or tasks file to use plugin FQCN
https://gist.github.com/sivel/1f850b7f577b9dc9466293034c82b19d

Make a disposition CSV for ansible content
https://gist.github.com/cidrblock/40a540c54abb6f8767f7da7a85c84a94

https://github.com/ansible-network/collection_prep




