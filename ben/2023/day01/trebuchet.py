from __future__ import annotations
import aoc
import itertools
import re
from typing import Generator


DIGIT_STRINGS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
DIGIT_CHARS = [str(n) for n in range(1, len(DIGIT_STRINGS) + 1)]
DIGIT_MAP = {k: v for k, v in zip(DIGIT_STRINGS, DIGIT_CHARS)} | {v: v for v in DIGIT_CHARS}

def pull_digits(calibrations: str, pattern: str) -> Generator[int]:
    matches = re.findall(pattern, calibrations)
    matches = (list(g) for k, g in itertools.groupby(matches, lambda x: x == '\n') if not k)
    for group in matches:
        yield int(DIGIT_MAP[group[0]] + DIGIT_MAP[group[-1]])


@aoc.register(__file__)
def answers():
    calibrations = aoc.read_data()

    pattern1 = fr'(?=(\n|\d))'
    yield sum(pull_digits(calibrations, pattern1))

    pattern2 = fr'(?=(\n|\d|{"|".join(list(DIGIT_STRINGS))}))'
    yield sum(pull_digits(calibrations, pattern2))

if __name__ == '__main__':
    aoc.run()
