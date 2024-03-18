import sys, logging, requests
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


def get_request(url: str, params: dict = None, **kwargs):
    try:
        response = requests.get(url, params=params, **kwargs)
        response.raise_for_status()
        return response
    except HTTPError:
        logger.exception('HTTP error')
        sys.exit(1)
    except Exception:
        logger.exception('Request error')
        sys.exit(1)


def get_api(params: dict, **kwargs):
    return get_request('https://en.wikipedia.org/w/api.php', params, **kwargs)
