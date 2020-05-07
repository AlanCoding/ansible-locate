from ansible.parsing.utils.yaml import from_yaml
from ansible.parsing.yaml.dumper import AnsibleDumper

from ansible_locate.plugin_routing import _get_tombstones
from ansible_locate.isms import could_be_yaml, could_be_role, could_be_playbook

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
                routing[key] = epitaphs[key]["redirect"]
    return routing


def inspect_task_list(filename, write_names=False):
    with open(filename, 'r') as f:
        content = f.read()
    try:
        data = from_yaml(content)
    except Exception:
        print(f'   could not read {filename} as YAML')
        return {}
    if not could_be_role(data):
        # print(f'  skipping file {subdir}/tasks/{filename} because it looks empty')
        return {}
    # else:
    #     print(f'  inspecting {subdir}/tasks/{filename}')
    return locate_tasks(data)


def inspect_playbook(playbook, write_names=False):
    routing = {}

    with open(playbook, 'r') as f:
        content = f.read()
    if not could_be_playbook(content):
        if could_be_role(content):
            print(f' inspecting as task list {playbook}')
            return inspect_task_list(playbook, write_names=write_names)
        print(f' skipping playbook {playbook}')
        return routing
    else:
        print(f' inspecting playbook {playbook}')
    try:
        data = from_yaml(content)
    except Exception:
        print(f'   could not read {playbook} as YAML')
        return routing
    # print('print data')
    # print(json.dumps(data, indent=2))
    for i, play in enumerate(data):
        tasks = get_tasks_from_play(play)
        # if not tasks:
        #     if 'name' in play:
        #         print(f' skipping {play["name"]} because tasks not found')
        #     else:
        #         print(f' skipping {i}th play because tasks not found')
        if tasks:
            new_routing = locate_tasks(tasks)
            routing.update(new_routing)
    return routing


def list_yaml(dir):
    r = []
    for f in os.listdir(dir):
        if not could_be_yaml(f):
            continue
        abs_path = os.path.join(dir, f)
        if os.path.isdir(abs_path):
            continue
        r.append(abs_path)
    return r


def crawl(location, write_meta=False):
    if os.path.isdir(location):
        print('Inspecting playbooks')
        playbook_dir = location
        routing = {}
        for filename in list_yaml(playbook_dir):
            new_routing = inspect_playbook(filename)
            for key, value in new_routing.items():
                print(f'   {key} --> {value}')
            routing.update(new_routing)
    else:
        print('Inspecting playbook {location}')
        playbook_dir = os.path.dirname(location)
        routing = inspect_playbook(location)
        for key, value in routing.items():
            print(f'   {key} --> {value}')

    # roles
    print('')
    roles_dir = os.path.join(playbook_dir, 'roles')
    if not os.path.exists(roles_dir):
        print('Found no roles dir, exiting')
        return
    else:
        print('Inspecting role directories')
    for subdir in os.listdir(roles_dir):
        role_dir = os.path.join(roles_dir, subdir)
        if not os.path.isdir(role_dir):
            continue
        tasks_dir = os.path.join(role_dir, 'tasks')
        # print(f' inspecting role {subdir}')
        if not os.path.exists(tasks_dir):
            continue
        role_routing = {}
        for filename in os.listdir(tasks_dir):
            file_path = os.path.join(tasks_dir, filename)
            if os.path.isdir(file_path):
                continue
            if not could_be_yaml(filename):
                continue
            new_routing = inspect_task_list(file_path)
            for key, value in new_routing.items():
                print(f'   roles/{subdir}/tasks/{filename}: {key} --> {value}')
            role_routing.update(new_routing)
        # print(' routing for role {subdir}:')
        # print(json.dumps(role_routing, indent=2))
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
                value.rsplit('.', 1)[0] for value in role_routing.values()
            )
            existing_data['collections'] = sorted(list(need_collections))

            if existing_data == {'collections': []}:
                if os.path.exists(meta_file):
                    os.remove(meta_file)
            else:
                with open(meta_file, 'w') as f:
                    f.write(yaml.dump(existing_data, Dumper=AnsibleDumper))

        routing.update(role_routing)

    print('')
    print('Overall routing:')
    print(json.dumps(routing, indent=2))

    print('')
    print('Collection needs:')
    needs = set(
        fqcn.rsplit('.', 1)[0] for fqcn in routing.values()
    )
    for need in needs:
        print(f'  - {need}')
    print('')
