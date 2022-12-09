import aoc
from math import prod
import numpy as np
from numpy.typing import NDArray


def visible_from_edge(trees: NDArray, rot: int) -> NDArray:
    ar = np.rot90(trees, rot)
    visible = np.full(ar.shape, False)
    visible[0] = True
    visible[1:] = ar[1:] > np.maximum.accumulate(ar, axis=0)[:-1]
    return np.rot90(visible, 4-rot)

def visible_from_tree(trees: NDArray, rot: int) -> NDArray:
    ar = np.rot90(trees, rot)
    def _on_row(i: int):
        chop = ar[i:]
        rolling_max = np.maximum.accumulate(chop[1:], axis=0)
        count = np.sum(chop[0] > rolling_max, axis=0)
        return np.where(count < len(chop)-1, count+1, count)
    
    vision = np.array([_on_row(i) for i in range(len(ar))])
    return np.rot90(vision, 4-rot)
        

@aoc.register(__file__)
def answers():
    trees = np.array(aoc.read_grid(), dtype=int)

    visible = [visible_from_edge(trees, i) for i in range(4)]
    yield np.count_nonzero(np.logical_or.reduce(visible))

    visible = [visible_from_tree(trees, i) for i in range(4)]
    yield np.max(prod(visible))

if __name__ == '__main__':
    aoc.run()
