import os, sys


def non_empty_input(prompt: str = ''):
    if prompt != '':
        print(prompt, end='')
    while True:
        inp = input()
        if inp != '':
            break
    return inp


def list_dirs(path: str) -> list:
    if not os.path.isdir(path):
        sys.exit('Directory does not exist!')
    if not path[-1] in ['/', '\\']:
        path += os.sep
    return [item for item in os.listdir(path) if os.path.isdir(path + item)]
