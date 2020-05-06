import argparse

from ansible_content_locator.crawler import crawl

parser = argparse.ArgumentParser(
    description=(
        'Locates* content you are using in a playbook. '
        'To locate means to identify in the collections world.'
    )
)
parser.add_argument('--write-meta', action='store_true')
# https://github.com/ansible/ansible/blob/devel/lib/ansible/cli/playbook.py
parser.add_argument('playbook', help='Playbook(s)', metavar='playbook', nargs=1)


def main():
    args = parser.parse_args()
    crawl(args.playbook[0], write_meta=args.write_meta)
