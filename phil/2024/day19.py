from functools import cache

@cache
def count(pat: str, towels: tuple) -> int:
    return sum(count(pat[len(t):], towels) for t in towels if pat.startswith(t)) if len(pat) > 0 else 1

def solve(puzzle_input: str) -> tuple[int]:
    towel_text, pattern_text = puzzle_input.split('\n\n')
    towels = tuple(towel_text.split(', '))
    a, b = 0, 0
    for pattern in pattern_text.splitlines():
        if (solutions := count(pattern, towels)) > 0:
            b += solutions
            a += 1
    return a, b

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "19.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
