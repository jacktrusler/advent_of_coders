import argparse
import cProfile
from pathlib import Path
import re
import time

from aoc.input import set_main_file
from aoc.register import registered_functions


NUM_WORDS = {1: 'ONE', 2: 'TWO'}

def get_answers(func):
    for i, answer in enumerate(func()):
        print(f'PART {NUM_WORDS[i+1]}: {answer}')
    

def run(profile: bool = False):
    for func, filename in registered_functions().items():
        set_main_file(filename)
        info = re.match(r'.*\\(?P<year>\d+)\\day(?P<day>\d+)\\(?P<filename>.*).py', filename).groupdict()
        print(f'********************************************')
        print(f'** {info["year"]}/day{info["day"]}: {info["filename"].replace("_", " ").title()}')

        if profile:
            pr = cProfile.Profile()
            pr.enable()

        start = time.perf_counter()
        for i, answer in enumerate(func()):
            print(f'PART {NUM_WORDS[i+1]}: {answer}')
        end = time.perf_counter()
        print(f'Time elapsed: {round((end - start) * 1000, 3)} ms')

        if profile:
            pr.disable()
            f = Path(filename)
            output = f.parent.joinpath(f'{f.stem}.pstats')
            pr.dump_stats(str(output))
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run advent of code files')
    parser.add_argument('-y', '--year', help='The year to run', type=int)
    parser.add_argument('-p', '--profile', help='Profile the run', default=False, action='store_true')
    args = vars(parser.parse_args())

    if (year := args.pop('year')) is not None:
        __import__(str(year))
    else:
        cwd = Path.cwd()
        dirs = [d.relative_to(cwd) for d in cwd.iterdir() if d.is_dir()]
        dirs = [d for d in dirs if not str(d).startswith('.') and str(d) != 'aoc']
        [__import__(str(d)) for d in dirs]
    run(**args)
