from pathlib import Path
import utils
import re
import itertools

def expand(data, empty_factor):
    empty_before = 0
    prev_x = 0
    for x in data:
        empty_before += max(x - prev_x - 1, 0)
        yield x + empty_before * empty_factor
        prev_x = x

def sum_distances(x, y, n):
    dx = sum(x2 - x1 for x1, x2 in itertools.combinations(expand(x, n), 2))
    dy = sum(y2 - y1 for y1, y2 in itertools.combinations(expand(sorted(y), n), 2))
    return dx + dy

def solve(raw_input: str):
    line_length = raw_input.index('\n') + 1
    galaxies = list(divmod(m.start(), line_length) for m in re.finditer(r'#', raw_input))
    galaxy_x, galaxy_y = zip(*galaxies)
    a = sum_distances(galaxy_x, galaxy_y, 1)
    b = sum_distances(galaxy_x, galaxy_y, 999999)
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "11.txt"
    utils.report(*utils.run_solution(solve, input_path))
