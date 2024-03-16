import sys, requests
from requests.exceptions import HTTPError


def get_request(url: str, params: dict = {}, **kwargs):
    try:
        response = requests.get(url, params=params, **kwargs)
        response.raise_for_status()
        return response
    except HTTPError as http_err:
        sys.exit(f'[HTTP ERR]: {http_err}')
    except Exception as err:
        sys.exit(f'[ERR]: {err}')


def get_api(params: dict, **kwargs):
    return get_request('https://en.wikipedia.org/w/api.php', params, **kwargs)
