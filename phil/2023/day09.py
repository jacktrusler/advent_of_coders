from pathlib import Path
import utils

def extrapolate(sequence: list) -> tuple[int, int]:
    next_sequence = [x - y for x, y in zip(sequence[1:], sequence[:-1])]
    start, end = extrapolate(next_sequence) if any(next_sequence) else (0, 0)
    return sequence[0] - start, sequence[-1] + end

def solve(raw_input: str):
    results = [extrapolate([int(x) for x in line.split()]) for line in raw_input.splitlines()]
    b, a = map(sum, zip(*results))
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "09.txt"
    utils.report(*utils.run_solution(solve, input_path))
