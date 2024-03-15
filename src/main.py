import re, sys

from wiki import *
from utils import *
from request import *


def main():
    page = where_it_all_begins()
    episodes = parse_episodes(page)
    results = check_results(episodes)
    path = non_empty_input('Please enter the path to the TV show folder: ')
    dirs = list_dirs(path)
    for folder in dirs:
        if re.search('^[Ss]\d{2,}.*', folder):
            print(f'  "{folder}"')
        else:
            dirs.remove(folder)
    if len(dirs) == 0:
        sys.exit('No season folder found!')
    choice = input('Proceed to rename? (y/n)')
    if not choice in ['y', 'Y', '']:
        sys.exit('Exiting...')
    # TODO: list each season and rename


if __name__ == '__main__':
    main()
