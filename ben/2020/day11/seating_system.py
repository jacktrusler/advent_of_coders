import aoc
import itertools
import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import convolve
from typing import Callable


FLOOR = 0
EMPTY = 1
OCCUPIED = 2

DIRECTIONS = [x for x in itertools.product((-1, 0, 1), repeat=2) if x != (0,0)]


def count_adjacent_seats(layout: NDArray) -> NDArray:
    window = np.array([[1,1,1], [1,0,1], [1,1,1]])
    return convolve(np.where(layout == OCCUPIED, 1, 0), window, mode='constant')

def count_seen_seats(layout: NDArray) -> int:
    def adjacent_seats(_layout: NDArray, dir: tuple[int, int]) -> NDArray:
        default_slice = (1,-1)
        vert = (default_slice[0] + dir[0], default_slice[1] + dir[0])
        horz = (default_slice[0] + dir[1], default_slice[1] + dir[1])
        vert_slice = slice(vert[0], None if vert[1] == 0 else vert[1])
        horz_slice = slice(horz[0], None if horz[1] == 0 else horz[1])
        return np.pad(_layout, 1)[vert_slice, horz_slice]

    def sightline(_layout: NDArray, dir: tuple[int, int]) -> NDArray:
        shifted = adjacent_seats(_layout, dir)
        retval = np.where(_layout == FLOOR, shifted, _layout)

        if not (_layout == retval).all():
            return sightline(retval, dir)
        return adjacent_seats(retval, dir) == OCCUPIED

    return sum([sightline(layout, d) for d in DIRECTIONS])

def process_seats(layout: NDArray, tolerance: int, count_method: Callable) -> NDArray:
     _layout = np.copy(layout)
     while True:
        count = count_method(_layout)
        step_one = np.where((_layout == EMPTY) & (count == 0), OCCUPIED, _layout)
        step_two = np.where((step_one == OCCUPIED) & (count >= tolerance), EMPTY, step_one)

        if (_layout == step_two).all():
            return _layout
        _layout = step_two


@aoc.register(__file__)
def answers():
    initial_layout = np.array(aoc.read_grid())
    initial_layout[initial_layout == '.'] = FLOOR
    initial_layout[initial_layout == 'L'] = EMPTY
    initial_layout = initial_layout.astype(int)

    layout1 = process_seats(initial_layout, tolerance=4, count_method=count_adjacent_seats)
    yield np.count_nonzero(layout1 == OCCUPIED)

    layout2 = process_seats(initial_layout, tolerance=5, count_method=count_seen_seats)
    yield np.count_nonzero(layout2 == OCCUPIED)

if __name__ == '__main__':
    aoc.run()
