import re, sys, bs4, logging

from request import get_api

logger = logging.getLogger(__name__)


def search(query: str, limit: int = 8) -> str:
    return get_api({
        'action': 'opensearch',
        'search': query,
        'limit': str(limit),
        'format': 'json'
    }).json()[1]


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
        logger.error('Episodes section not found on the wiki page!')
        sys.exit(1)
    return index


def check_external_episodes_article(page: str) -> str | None:
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
                logger.debug(f'Unknown scenario while parsing episode name: "{column}"')
        except (AttributeError, KeyError):
            logger.exception('Exception while parsing episode names')
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


def check_fails(episodes: dict) -> int:
    failed = 0
    for names in episodes.values():
        for name in names:
            if not name:
                failed += 1
    failed and logger.warning(f'Failed to retrieve {failed} episode name(s)')
    return failed
