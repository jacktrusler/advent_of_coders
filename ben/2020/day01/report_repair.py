import aoc
import itertools
from math import prod


def find_combo(data: list[int], target: int, len: int) -> int:
    for combo in itertools.combinations(data, len):
        if sum(combo) == target:
            return prod(combo)

@aoc.register(__file__)
def answers():
    data = list(map(int, aoc.read_lines()))
    yield find_combo(data, 2020, 2)
    yield find_combo(data, 2020, 3)

if __name__ == '__main__':
    aoc.run()
