import re, os, sys, logging

INDENT = ' ' * 2

logger = logging.getLogger(__name__)


def non_empty_input(prompt: str = None):
    prompt and print(prompt, end='')
    while True:
        _input = input()
        if _input:
            break
    return _input


def bool_input(prompt: str = None):
    prompt and print(f'{prompt} (y/n)', end='')
    return re.match(r'^(?:Y(?:es)?)?$', input(), re.I)


def list_dirs(path: str) -> list:
    if not os.path.isdir(path):
        logger.error('User-provided series folder does not exist!')
        sys.exit(1)
    if not path[-1] in ['/', '\\']:
        path += os.sep
    return [item for item in os.listdir(path) if os.path.isdir(path + item)]
