

def could_be_yaml(filename):
    return bool('.yml' in filename or '.yaml' in filename)


def could_be_playbook(data):
    for phrase in ('hosts', 'include', 'import_playbook'):
        if phrase in data:
            return True
    return False


def could_be_role(data):
    if not isinstance(data, list):
        return False
    return all(isinstance(task, dict) for task in data)
