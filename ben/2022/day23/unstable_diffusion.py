import aoc
from collections import Counter
from enum import Enum
from itertools import cycle, islice
import numpy as np
from numpy.typing import NDArray
from typing import Iterable


class Direction(Enum):
    NORTH = (-1, 0)
    SOUTH = (1, 0)
    WEST = (0, -1)
    EAST = (0, 1)


WINDOWS = {
    Direction.NORTH: [[0,0,0],[0,0,0],[1,1,1]],
    Direction.SOUTH: [[1,1,1],[0,0,0],[0,0,0]],
    Direction.WEST:  [[0,0,1],[0,0,1],[0,0,1]],
    Direction.EAST:  [[1,0,0],[1,0,0],[1,0,0]],
}
def check_adjacent(grid: NDArray, dir: Direction = None):
    kwargs = {} if dir is None else {'window': WINDOWS[dir]}
    check = aoc.np.count_adjacent(grid, **kwargs)
    return set(zip(*np.where((grid > 0) & (check == 0))))

def scrunch(ar: NDArray) -> NDArray:
    def first_value(_ar: NDArray) -> int:
        for i, r in enumerate(_ar):
            if 1 in r:
                return i
    up = first_value(ar)
    down = len(ar) - first_value(ar[::-1])
    left = first_value(ar.T)
    right = len(ar.T) - first_value(ar.T[::-1])
    return ar[up:down, left:right]

def perform_round(ar: NDArray, dirs: Iterable[Direction]) -> NDArray:
    _ar = np.pad(ar, 1, mode='constant', constant_values=0)
    movements = {elf: elf for elf in check_adjacent(_ar)}
    for d in dirs:
        movers = check_adjacent(_ar, d)
        movers = movers - set(movements.keys())
        movements.update({elf: (elf[0] + d.value[0], elf[1] + d.value[1]) for elf in movers})

    count = Counter(movements.values())
    movements = {k: v for k, v in movements.items() if count[v] == 1}

    old_pos = tuple(map(list, zip(*movements.keys())))
    new_pos = tuple(map(list, zip(*movements.values())))
    _ar[old_pos] = 0
    _ar[new_pos] = 1
    return scrunch(_ar)

@aoc.register(__file__)
def answers():
    grid = np.where(np.asarray(aoc.read_grid()) == '#', 1, 0)
    dirs = np.array(list(Direction))

    i = 0
    while True:
        i += 1
        _grid = perform_round(grid, dirs)
        if np.array_equal(grid, _grid):
            break

        grid = _grid
        if i == 10:
            yield np.sum(grid == 0)
        dirs = np.roll(dirs, -1)
    yield i


if __name__ == '__main__':
    aoc.run(profile=True)
