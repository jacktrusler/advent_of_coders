from pathlib import Path
import utils

def tilt_left(items: str) -> str:
    new_items = ''
    rocks = ''
    blanks = ''
    for char in items:
        match char:
            case 'O':
                rocks += 'O'
            case '.':
                blanks += '.'
            case '#':
                new_items += rocks + blanks + '#'
                rocks = ''
                blanks = ''
    new_items += rocks + blanks
    return new_items

def transpose(x: tuple) -> tuple:
    return tuple(map(''.join, zip(*x)))

def north(grid: tuple) -> tuple:
    return transpose(west(transpose(grid)))

def south(grid: tuple) -> tuple:
    return transpose(east(transpose(grid)))

def east(grid: tuple) -> tuple:
    return tuple(tilt_left(row[::-1])[::-1] for row in grid)

def west(grid: tuple) -> tuple:
    return tuple(tilt_left(row) for row in grid)

def score(grid: tuple) -> int:
    return sum([(len(grid) - i) * row.count('O') for i, row in enumerate(grid)])

def i_matching(n: int, a: int, b: int) -> int:
    """Return an index in range [a, b] of a value in a cyclical iterable at n if the items at a and b are equal"""
    return ((n - b) % (a - b)) + b

def cycle_grids(grid: tuple):
    i = 0
    yield i, grid
    while True:
        i += 1
        grid = east(south(west(north(grid))))
        yield i, grid

def solve(raw_input: str) -> tuple[int, int]:
    grids = dict()
    for i, grid in cycle_grids(tuple(raw_input.splitlines())):
        try:
            i_match = grids[grid]
        except KeyError:
            grids[grid] = i
        else:
            break
    grid_lookup = {v: k for k, v in grids.items()}
    a = score(north(grid_lookup[0]))
    b = score(grid_lookup[i_matching(1000000000, i, i_match)])
    return a, b

if __name__ == '__main__':
    input_path = Path(__file__).parent / "input" / "14.txt"
    utils.report(*utils.run_solution(solve, input_path))
