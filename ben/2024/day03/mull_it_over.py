import aoc
import re
from typing import Match, Iterable, Iterator


def process_mul(instruction: Match[str]) -> int:
    data = instruction.groupdict()
    return int(data['x']) * int(data['y'])

def process_do_dont(instructions: Iterable[Match[str]]) -> Iterator[int]:
    active = True
    for x in instructions:
        inst = x.group(0)
        if inst.startswith('mul') and active:
            yield process_mul(x)
        elif inst == "do()":
            active = True
        elif inst == "don't()":
            active = False

@aoc.register(__file__)
def answers():
    memory = aoc.read_data()

    # Part One
    mul_regex = r'mul\((?P<x>\d{1,3}),(?P<y>\d{1,3})\)'
    instructions = (x for x in re.finditer(f'({mul_regex})', memory))
    yield sum(process_mul(x) for x in instructions)

    # Part Two
    do_dont_regex = r'do\(\)|don\'t\(\)'
    instructions = (x for x in re.finditer(f'({mul_regex}|{do_dont_regex})', memory))
    yield sum(process_do_dont(instructions))

if __name__ == '__main__':
    aoc.run()
