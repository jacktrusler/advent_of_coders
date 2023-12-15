from pathlib import Path
import utils
import functools

@functools.cache
def tilt_chunk(chunk: str) -> str:
    num_rocks = chunk.count('O')
    return 'O' * num_rocks + '.' * (len(chunk) - num_rocks)

@functools.cache
def tilt_line(line: str) -> str:
    return ''.join(tilt_chunk(chunk) + '#' for chunk in line.split("#"))[:-1]

def tilt_grid(grid: tuple):
    return tuple(tilt_line(row) for row in grid)

def rotate(grid: tuple) -> tuple:
    return tuple(map(lambda x: ''.join(x)[::-1], zip(*grid)))

def score(grid: tuple) -> int:
    return sum([(len(grid) - i) * row.count('O') for i, row in enumerate(rotate(grid))])

def cycle_grids(grid: tuple):
    yield grid
    while True:
        for _ in range(4):
            grid = rotate(tilt_grid(grid))
        yield grid

def solve(raw_input: str) -> tuple[int, int]:
    grids = dict()
    grid = rotate(rotate(rotate(tuple(raw_input.splitlines()))))  # left is north
    for i, grid in enumerate(cycle_grids(grid)):
        try:
            i_match = grids[grid]
        except KeyError:
            grids[grid] = i
        else:
            break
    grid_lookup = {v: k for k, v in grids.items()}
    a = score(tilt_grid(grid_lookup[0]))
    b = score(grid_lookup[((1000000000 - i_match) % (i - i_match)) + i_match])
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "14.txt"
    utils.report(*utils.run_solution(solve, input_path))
