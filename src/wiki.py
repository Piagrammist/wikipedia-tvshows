import re, sys, bs4

from utils import non_empty_input
from request import get_api

INDENT = ' ' * 2


def find_page(query: str) -> str:
    titles = get_api({
        'action': 'opensearch',
        'search': query,
        'limit': '8',
        'format': 'json'
    }).json()[1]
    print('Please choose the right TV show:')
    target = -1
    for i, title in enumerate(titles):
        print(f'{INDENT}{i + 1}. {title}', end='')
        if target == -1 and title.lower().find('tv series') != -1:
            target = i
            print(' <---', end='')
        print()
    if target != -1:
        print('Press Enter to continue... Or choose another item instead: ', end='')
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


def where_it_all_begins() -> str:
    while True:
        choice = input('Proceed to automatic search or manual URL input? (a/m) ')
        if choice in ['a', 'A']:
            name = non_empty_input('Please enter the TV show name: ')
            page = find_page(name)
            break
        elif choice in ['m', 'M']:
            url = non_empty_input('Please enter the Wikipedia link of the show: ')
            match = re.match(r'^(?:(?:https?:)?//)?(?:\w+\.)?wikipedia\.org/wiki/(\w+_\(\w*TV_series\))(?:#.+)?$', url)
            if not match:
                sys.exit('[ERR]: Wrong URL provided!')
            page = match.group(1)
            break
    return page


def find_episodes_section_index(page: str) -> int:
    sections = get_api({
        'action': 'parse',
        'page': page,
        'format': 'json',
        'prop': 'sections'
    }).json()['parse']['sections']
    index = -1
    for section in sections:
        if section['anchor'] == 'Episodes':
            index = section['index']
            break
    if index == -1:
        sys.exit('[ERR]: Episodes section not found on the wiki page!')
    return index


def check_external_episodes_article(page: str):
    html = get_api({
        'action': 'parse',
        'page': page,
        'format': 'json'
    }).json()['parse']['text']['*']
    soup = bs4.BeautifulSoup(html, 'html.parser')
    hatnotes = soup.find_all('div', attrs={'class': 'hatnote', 'role': 'note'})
    external_article = None
    for hatnote in hatnotes:
        if hatnote.contents[1].name == 'a' and re.match(r'^List of .+ episodes$', hatnote.a.string):
            external_article = hatnote.a.attrs['href'].split('/')[-1]
            break
    return external_article


def parse_episodes_table(table: bs4.Tag) -> list:
    episodes = []
    for row in table.tbody.find_all('tr', class_='vevent'):
        column = row.find('td', class_='summary')
        name = ''
        try:
            if column.string:             # normal
                name = column.string
            elif column.a:                # linked
                name = column.a.string
            elif column.span:             # bilingual
                name = column.contents[0]
                if name == '"':           # bilingual (translated alongside `abbr` tag)
                    name = column.contents[1].i.string
            else:
                print(f'[ERR]: Could not extract name from "{column}"!')
        except (AttributeError, KeyError) as e:
            print(f'[ERR]: {e}')
        episodes.append(name.replace('"', '').strip())
    return episodes


def parse_episode_tables(html: str) -> dict:
    soup = bs4.BeautifulSoup(html, 'html.parser')
    seasons = {}
    for i, table in enumerate(soup.find_all('table', class_='wikiepisodetable')):
        seasons[str(i + 1)] = parse_episodes_table(table)
    return seasons


def parse_internal_episode_tables(page: str) -> dict:
    html = get_api({
        'action': 'parse',
        'page': page,
        'format': 'json',
        'section': find_episodes_section_index(page)
    }).json()['parse']['text']['*']
    return parse_episode_tables(html)


def parse_episodes(page: str) -> dict:
    external_article = check_external_episodes_article(page)
    return parse_episodes(external_article)\
        if external_article\
        else parse_internal_episode_tables(page)


def check_results(episodes: dict):
    results = {True: 0, False: 0}
    for names in episodes.values():
        for name in names:
            results[False if name == '' else True] += 1
    print(f'Total: {results[True] + results[False]}' +
          f'\n{INDENT}Success: {results[True]}' +
          f'\n{INDENT}Fail: {results[False]}')
    return results
