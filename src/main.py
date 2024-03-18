import re, sys

from wiki import *
from utils import *
from request import *


def main():
    page = where_it_all_begins()
    episodes = parse_episodes(page)
    results = check_results(episodes)
    if results[False] > 0 and not bool_input('Failed to retrieve one or more episode names. Continue?'):
        sys.exit(1)
    path = non_empty_input('Please enter the path to the TV show folder: ')
    dirs = list_dirs(path)
    if len(dirs) == 0:
        sys.exit('No season folder found!')
    for folder in dirs:
        if re.match(r'^[Ss]\d{2,}.*', folder):
            print(f'  "{folder}"')
        else:
            dirs.remove(folder)
    if not bool_input('Proceed to rename?'):
        sys.exit('Exiting...')
    # TODO: list each season and rename


if __name__ == '__main__':
    main()
