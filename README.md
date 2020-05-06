# Ansible Content Locator

This is a tool which will walk around the YAML files in your playbook project
and then suggest where to get that content from collections.

```
ansible-locate install.yml
```

Will just print stuff. This may give you enough information to
`ansible-galaxy collection install` the collections needed for your stuff
to run.

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

