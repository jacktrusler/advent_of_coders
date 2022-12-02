import argparse
from pathlib import Path
import shutil


def create(year: int, day: int, name: str):
    year_dir = Path.cwd().joinpath(str(year))
    if not year_dir.exists():
        year_dir.mkdir()
        template_init = Path.cwd().joinpath('aoc/template_init.py')
        dest_init = year_dir.joinpath('__init__.py')
        shutil.copy(str(template_init), str(dest_init))

    day_dir = year_dir.joinpath('day{:02d}'.format(day))
    if not day_dir.exists():
        day_dir.mkdir()

    small_file = day_dir.joinpath('small.txt')
    data_file = day_dir.joinpath('data.txt')
    with open(small_file, mode='w') as f: pass
    with open(data_file, mode='w') as f: pass

    template_py = Path.cwd().joinpath('aoc/template_py.py')
    dest_py = day_dir.joinpath(f'{name}.py')
    shutil.copy(str(template_py), str(dest_py))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new Advent of Code folder and associated files')
    parser.add_argument('-y', '--year', help='The year to place the new files under', required=True, type=int)
    parser.add_argument('-d', '--day', help='The day to place the new files under', required=True, type=int)
    parser.add_argument('-n', '--name', help='The name of the new file', required=True)
    args = vars(parser.parse_args())
    create(**args)
