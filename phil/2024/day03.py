import re

def solve(puzzle_input: str):
    a = 0
    b = 0
    enabled = True
    for m in re.finditer("(do\(\)|don't\(\)|mul\((\d+),(\d+)\))", puzzle_input):
        match m.groups():
            case ["do()", *_]:
                enabled = True
            case ["don't()", *_]:
                enabled = False
            case [_, x, y]:
                prod = int(x) * int(y)
                a += prod
                if enabled:
                    b += prod
    return a, b

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "03.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
