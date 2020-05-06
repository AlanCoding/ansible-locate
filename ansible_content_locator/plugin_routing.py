# (c) 2019 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import sys
import yaml

from ansible.errors import AnsibleInternalError

_tombstones = None


def _get_tombstones():
    # FUTURE: thread safety, string cleanup, validation
    global _tombstones
    if not _tombstones:
        try:
            # can't use get_data here, as it causes a circular import
            ts_path = os.path.join(os.path.dirname(sys.modules['ansible'].__file__), 'config/routing.yml')
            with open(ts_path, 'r') as tsfd:
                _tombstones = yaml.safe_load(tsfd)
        except Exception as ex:
            raise AnsibleInternalError('Error parsing tombstone data: {0}'.format(str(ex)))

    return _tombstones
