import aoc
from functools import lru_cache
from math import prod
import numpy as np
from numpy.typing import NDArray


@lru_cache
def shift_slice(dir: tuple) -> tuple[slice, slice]:
    default_slice = (1,-1)
    vert = (default_slice[0] - dir[0], default_slice[1] - dir[0])
    horz = (default_slice[0] - dir[1], default_slice[1] - dir[1])
    vert_slice = slice(vert[0], None if vert[1] == 0 else vert[1])
    horz_slice = slice(horz[0], None if horz[1] == 0 else horz[1])
    return vert_slice, horz_slice

def shift(ar: NDArray, dir: tuple, pad: int) -> NDArray:
    vert_slice, horz_slice = shift_slice(dir)
    return np.pad(ar, 1, constant_values=pad)[vert_slice, horz_slice]

def visible_from_edge(ar: NDArray, dir: tuple) -> NDArray:
    def _visible(_layout):
        shifted = shift(_layout, dir, pad=-1)
        visible = np.where(shifted > _layout, shifted, _layout)
        if not (_layout == visible).all():
            return _visible(visible)
        return visible > shifted
    return _visible(ar)

def visible_from_tree(ar: NDArray, dir: tuple) -> NDArray:
    checker = ar.copy()

    def _count_visible(_layout, count=np.full_like(ar, 0)):
        shifted = shift(_layout, dir, pad=10)
        count[(checker > -1) & (shifted < 10)] += 1
        checker[checker <= shifted] = -1
        if (checker == -1).all():
            return count
        return _count_visible(shifted, count)
    return _count_visible(ar)
        

@aoc.register(__file__)
def answers():
    trees = np.array(aoc.read_grid(), dtype=int)
    directions = ((1,0), (-1,0), (0,1), (0,-1))

    visible = [visible_from_edge(trees, dir) for dir in directions]
    yield np.count_nonzero(np.logical_or.reduce(visible))

    visible = [visible_from_tree(trees, dir) for dir in directions]
    yield np.max(prod(visible))

if __name__ == '__main__':
    aoc.run()
