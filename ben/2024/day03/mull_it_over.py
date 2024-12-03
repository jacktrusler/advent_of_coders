import aoc
from aoc.utils import Interval
import re
from typing import Match, Iterator, Iterable


def process_mul(instruction: Match[str]) -> int:
    data = instruction.groupdict()
    return int(data['x']) * int(data['y'])

def valid_intervals(dos_and_donts: Iterable[Match[str]]) -> Iterator[Interval]:
    state = True
    prev = 0
    instruction = None

    for instruction in dos_and_donts:
        if not state and instruction.group(1) == 'do()':
            state = True
            prev = instruction.end()
        elif state and instruction.group(1) == "don't()":
            state = False
            yield Interval(prev, instruction.start())

    if state and instruction:
        yield Interval(prev, len(instruction.string))

@aoc.register(__file__)
def answers():
    memory = aoc.read_data()

    # Part One
    mul_instructions = [x for x in re.finditer(r'(mul\((?P<x>\d{1,3}),(?P<y>\d{1,3})\))', memory)]
    yield sum(process_mul(x) for x in mul_instructions)

    # Part Two
    intervals = list(valid_intervals(x for x in re.finditer(r'(do\(\)|don\'t\(\))', memory)))
    yield sum(process_mul(x) for x in mul_instructions if any(x.start() in y for y in intervals))

if __name__ == '__main__':
    aoc.run()
