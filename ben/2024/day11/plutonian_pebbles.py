import aoc
from collections import defaultdict
from functools import reduce, cache


@cache
def new_stones(stone: int) -> tuple[int]:
    if stone == 0:
        return 1,
    if (_len := len(stone_str := str(stone))) % 2 == 0:
        return int(stone_str[:_len // 2]), int(stone_str[_len // 2:])
    return 2024 * stone,

def blink(counter: dict) -> dict:
    new_count = defaultdict(int)
    for k, v in counter.items():
        for new_v in new_stones(k):
            new_count[new_v] += v
    return new_count

@aoc.register(__file__)
def answers():
    stones = defaultdict(int)
    for stone in aoc.read_data().split():
        stones[int(stone)] += 1

    # Part One
    stones = reduce(lambda x, _: blink(x), range(25), stones)
    yield sum(stones.values())

    # Part Two
    stones = reduce(lambda x, _: blink(x), range(50), stones)
    yield sum(stones.values())

if __name__ == '__main__':
    aoc.run()
