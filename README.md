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

Some specifics may be removed here, as non-public content

```
$ ansible-locate ~/Documents/repos/engineering/do_stuff.yml
Locked and loaded with 3752 module redirects

Inspecting playbook /Users/alancoding/Documents/repos/ansible-engineering/build_awx_production_images.yml
 skipping Build and push AWX Production Container Images because tasks not found
   roles/create_ec2_instances/tasks/main.yml: ec2 --> amazon.aws.ec2
   roles/access/tasks/main.yml: authorized_key --> ansible.posix.authorized_key
   roles/build_official_image/tasks/main.yml: docker_login --> community.general.docker_login
   roles/prepare-workspace/tasks/main.yaml: synchronize --> ansible.posix.synchronize
```

