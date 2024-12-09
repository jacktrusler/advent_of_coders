import aoc
from aoc.grid import Grid, Point
import itertools


def count_xmas(row: list[int]) -> int:
    arr_as_str = ''.join(row)
    return arr_as_str.count('XMAS') + arr_as_str.count('SAMX')

def is_x_mas(grid: Grid[int], point: Point) -> bool:
    try:
        diag_one = grid[point + (-1, -1), point + (1, 1)]
        diag_two = grid[point + (-1, 1), point + (1, -1)]
    except IndexError:
        return False
    return 'M' in diag_one and 'S' in diag_one and 'M' in diag_two and 'S' in diag_two

@aoc.register(__file__)
def answers():
    word_search = Grid[str](aoc.read_grid())
    
    # Part One
    all_dirs = word_search.rows(), word_search.columns(), word_search.diagonals(), word_search.diagonals(forward=False)
    yield sum(count_xmas(x) for x in itertools.chain(*all_dirs))

    # Part Two
    yield sum(is_x_mas(word_search, p) for p in word_search.find('A'))

if __name__ == '__main__':
    aoc.run()
