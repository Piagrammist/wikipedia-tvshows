import re, sys, logging
import wiki, utils
from utils import INDENT

logger = logging.getLogger(__name__)


def main():
    page = retrieve_page_name()
    episodes = wiki.parse_episodes(page)
    failed = wiki.check_fails(episodes)
    if failed and not utils.bool_input('Failed to retrieve one or more episode names. Continue?'):
        sys.exit(1)
    path = utils.non_empty_input('Please enter the path to the TV show folder: ')
    dirs = utils.list_dirs(path)
    if len(dirs) == 0:
        logger.error('No season folder found!')
        sys.exit(1)
    logger.info('Parsing directories...')
    for folder in dirs:
        if re.match(r'^[Ss]\d{2,}\. ', folder):
            logger.info(f'{INDENT}"{folder}"')
        else:
            dirs.remove(folder)
            logger.debug(f'Removed "{folder}" season folder due to invalid name pattern')
    if not utils.bool_input('Proceed to rename?'):
        logger.debug('Exiting before rename process due to user input')
        sys.exit('Exiting...')
    # TODO: list each season and rename


def retrieve_page_name() -> str:
    while True:
        choice = input('Proceed to automatic search or manual URL input? (a/m) ')
        if choice in ['a', 'A']:
            name = utils.non_empty_input('Please enter the TV show name: ')
            page = choose_page(name)
            break
        elif choice in ['m', 'M']:
            url = utils.non_empty_input('Please enter the Wikipedia link of the show: ')
            match = re.match(r'^(?:(?:https?:)?//)?(?:\w+\.)?wikipedia\.org/wiki/(\w+_\(\w*TV_series\))(?:#.+)?$', url)
            if not match:
                logger.error('Wrong Wikipedia URL provided!')
                sys.exit(1)
            page = match.group(1)
            break
    return page


def choose_page(query: str) -> str:
    titles = wiki.search(query)
    print('Please choose the right TV show:')
    target = -1
    for i, title in enumerate(titles):
        print(f'{INDENT}{i + 1}. {title}', end='')
        if target == -1 and title.lower().find('tv series') != -1:
            target = i
            print(' <---', end='')
        print()
    if target == -1:
        print('Choose an item: ', end='')
    else:
        print('Press Enter to continue. Or choose another item instead: ', end='')
    while True:
        choice = input()
        if choice == '' and target != -1:
            break
        elif choice.isnumeric() and 0 < int(choice) < 9:
            target = int(choice) - 1
            break
        else:
            print('Please enter a number ranging from 1-8: ', end='')
    return titles[target]
