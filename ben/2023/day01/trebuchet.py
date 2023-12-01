from __future__ import annotations
import aoc
import itertools
import re
from typing import Generator


DIGIT_STRINGS = {
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def pull_digits(calibrations: str, pattern: str) -> Generator[int]:
    matches = re.findall(pattern, calibrations)
    for key, group in itertools.groupby(matches, lambda x: x == '\n'):
        if key:
            continue
        group = list(group)
        first = DIGIT_STRINGS.get(group[0], group[0])
        last = DIGIT_STRINGS.get(group[-1], group[-1])
        yield int(f'{first}{last}')


@aoc.register(__file__)
def answers():
    calibrations = aoc.read_data()

    pattern1 = fr'(?=(\n|\d))'
    yield sum(pull_digits(calibrations, pattern1))

    pattern2 = fr'(?=(\n|\d|{"|".join(list(DIGIT_STRINGS.keys()))}))'
    yield sum(pull_digits(calibrations, pattern2))

if __name__ == '__main__':
    aoc.run()
