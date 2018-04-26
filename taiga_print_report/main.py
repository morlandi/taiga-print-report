#!/usr/bin/env python
import argparse
import sys
from .config_file import read_config_file
from .print_report import print_project


def check_python_taiga():
    from taiga.models import UserStory
    try:
        from taiga.models import Epic
    except ImportError as e:
        print("""
A specific python-taiga fork is required;
please manually install it as follows:

$ pip install git+https://github.com/morlandi/python-taiga.git
""")
        return False
    return True


def main():

    if not check_python_taiga():
        return

    # Read config file
    config = read_config_file()
    host = config.get('general', 'host').strip()
    username = config.get('general', 'username').strip()
    password = config.get('general', 'password').strip()
    copyright = config.get('general', 'copyright').strip()

    # See: https://docs.python.org/2/library/argparse.html
    parser = argparse.ArgumentParser(description='Extract printable report from Taiga Project')

    parser.add_argument('--host', help="if specified, overrides configured value")
    parser.add_argument('--username', help="if specified, overrides configured value")
    parser.add_argument('--password', help="if specified, overrides configured value")
    parser.add_argument('--copyright', help="if specified, overrides configured value")

    parser.add_argument('--project', default='')
    parser.add_argument('--summary', '-s', action='store_true', help="Export CSV summary instead of HTML document")
    parser.add_argument('--group-by-epics', '-e', action='store_true', help="Group user stories by epic (default is by Milestones")
    parser.add_argument('--wiki', '-w', action='store_true', help="Print wiki pages")
    parser.add_argument('--tasks', '-t', action='store_true', help="Include tasks")
    # parser.add_argument('--us', type=int, metavar='USER_STORY_FILTER', help="Filter a specific user story")
    # parser.add_argument('--ep', type=int, metavar='EPIC_FILTER', help="Filter a specific epic")
    args = parser.parse_args()

    if args.host:
        host = args.host
    if args.username:
        host = args.username
    if args.password:
        host = args.password
    if args.copyright:
        host = args.copyright

    sys.stderr.write('work in progress ...\n')
    print_project(
        host=host,
        username=username,
        password=password,
        project_slug_or_name=args.project,
        summary=args.summary,
        print_wiki_pages=args.wiki,
        include_tasks=args.tasks,
        copyright=copyright,
        group_by_epics=args.group_by_epics,
        task_headers=[
            config.get('task_headers', '0').strip(),
            config.get('task_headers', '1').strip(),
        ],
    )
    sys.stderr.write('Done.\n')

if __name__ == "__main__":
    main()
