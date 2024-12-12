from collections import defaultdict
from functools import cache
import aoc

@cache
def update_stone(stone: int) -> tuple:
    if stone == 0:
        return 1,
    elif len(str(stone)) % 2 == 0:
        stonestring = str(stone)
        stonelen = len(stonestring) // 2
        return int(stonestring[:stonelen]), int(stonestring[stonelen:])
    else:
        return stone * 2024,

def blink(stones: dict) -> dict:
    newstones = defaultdict(int)
    for stone, count in stones.items():
        for newstone in update_stone(stone):
            newstones[newstone] += count
    return newstones

def solve(puzzle_input: str):
    stones = defaultdict(int)
    for x in puzzle_input.split():
        stones[int(x)] += 1
    for _ in range(25):
        stones = blink(stones)
    a = sum(stones.values())
    for _ in range(50):
        stones = blink(stones)
    b = sum(stones.values())
    return a, b

@aoc.register(__file__)
def answers():
    a, b = solve(aoc.read_data())
    yield a
    yield b

if __name__ == '__main__':
    aoc.run()