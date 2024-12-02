from pathlib import Path
import aoc_util
from collections import Counter

def solve(puzzle_input: str):
    numbers = [int(x) for x in puzzle_input.split()]
    left = Counter(numbers[::2])
    right = Counter(numbers[1::2])
    a = sum(abs(x - y) for x, y in zip(sorted(left.elements()), sorted(right.elements())))
    b = sum(k * v * right[k] for k, v in left.items())
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "01.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
