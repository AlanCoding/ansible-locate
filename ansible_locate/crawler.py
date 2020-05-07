from ansible.parsing.utils.yaml import from_yaml
from ansible.parsing.yaml.dumper import AnsibleDumper

from ansible_locate.plugin_routing import _get_tombstones

import json
import yaml

import os


tombstones = _get_tombstones()
epitaphs = tombstones['plugin_routing']['modules']

print('Locked and loaded with {} module redirects'.format(len(epitaphs)))
print('')


def get_tasks_from_play(play):
    tasks = []
    for name in ('pre_tasks', 'tasks', 'post_tasks'):
        if name in play:
            tasks.extend(play[name])
    return tasks


def locate_tasks(tasks):
    routing = {}
    for task in tasks:
        for key in task:
            if key in epitaphs:
                print(f'   found {key}! moved to {epitaphs[key]["redirect"]}')
                routing[key] = epitaphs[key]["redirect"]
    return routing


def crawl(playbook, write_meta=False):
    print(f'Inspecting playbook {playbook}')
    with open(playbook, 'r') as f:
        content = f.read()
    data = from_yaml(content)
    # print('print data')
    # print(json.dumps(data, indent=2))
    for i, play in enumerate(data):
        tasks = get_tasks_from_play(play)
        if not tasks:
            if 'name' in play:
                print(f' skipping {play["name"]} because tasks not found')
            else:
                print(f' skipping {i}th play because tasks not found')
        else:
            locate_tasks(tasks)

    # roles
    d = os.path.dirname(playbook)
    roles_dir = os.path.join(d, 'roles')
    if not os.path.exists(roles_dir):
        print('Found no roles dir, exiting')
        return
    for subdir in os.listdir(roles_dir):
        role_dir = os.path.join(roles_dir, subdir)
        if not os.path.isdir(role_dir):
            continue
        tasks_dir = os.path.join(role_dir, 'tasks')
        print(f' inspecting role {subdir}')
        if not os.path.exists(tasks_dir):
            continue
        routing = {}
        for filename in os.listdir(tasks_dir):
            file_path = os.path.join(tasks_dir, filename)
            if os.path.isdir(file_path):
                continue
            if not (filename.endswith('yml') or filename.endswith('yaml')):
                continue
            with open(file_path, 'r') as f:
                content = f.read()
            data = from_yaml(content)
            if data is None:
                print(f'  skipping file {subdir}/tasks/{filename} because it looks empty')
                continue
            else:
                print(f'  inspecting {subdir}/tasks/{filename}')
            new_routing = locate_tasks(data)
            routing.update(new_routing)
        print(' routing for role {subdir}:')
        print(json.dumps(routing, indent=2))
        if write_meta:
            if not os.path.exists(os.path.join(role_dir, 'meta')):
                continue
            meta_file = os.path.join(role_dir, 'meta', 'main.yml')
            if os.path.exists(meta_file):
                with open(meta_file, 'r') as f:
                    existing_content = f.read()
                existing_data = from_yaml(existing_content)
            else:
                existing_data = {}
            need_collections = set(
                value.rsplit('.', 1)[0] for value in routing.values()
            )
            print(need_collections)
            existing_data['collections'] = sorted(list(need_collections))

            if existing_data == {'collections': []}:
                if os.path.exists(meta_file):
                    os.remove(meta_file)
            else:
                with open(meta_file, 'w') as f:
                    f.write(yaml.dump(existing_data, Dumper=AnsibleDumper))

