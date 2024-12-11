from collections import defaultdict
from functools import cache

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

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "11.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
