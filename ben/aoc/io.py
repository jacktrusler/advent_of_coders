from pathlib import Path


MAIN_FILE = None
def set_main_file(filename):
    global MAIN_FILE
    MAIN_FILE = filename

def _data_file(filename) -> str:
    return str(Path(MAIN_FILE).parent.joinpath(f'{filename}.txt'))

def read_data(filename='data') -> str:
    with open(_data_file(filename)) as f:
        data = f.read()
    return data

def read_lines(filename='data') -> list[str]:
    with open(_data_file(filename)) as f:
        data = f.read().splitlines()
    return data

def read_chunks(filename='data') -> list[str]:
    with open(_data_file(filename)) as f:
        data = f.read().split('\n\n')
    return data

def read_grid(filename='data') -> list[list[str]]:
    with open(_data_file(filename)) as f:
        data = list(map(list, f.read().splitlines()))
    return data
