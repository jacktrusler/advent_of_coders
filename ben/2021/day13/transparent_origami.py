import aoc
from functools import reduce
import numpy as np
from numpy.typing import NDArray


def fold(points: NDArray, idx: int, line: int) -> NDArray:
    retval = points.copy()
    retval[idx] = line - abs(retval[idx] - line)
    return np.unique(retval, axis=1)


@aoc.register(__file__)
def answers():
    points, folds = aoc.read_chunks()
    points = np.array([list(map(int, x.split(','))) for x in points.splitlines()], dtype=int).T
    folds = [tuple(x.replace('fold along ', '').split('=')) for x in folds.splitlines()]
    folds = [(0 if axis == 'x' else 1, int(line)) for axis, line in folds]

    points = fold(points, *folds.pop(0))
    yield points.shape[1]

    points = reduce(lambda x,y: fold(x, *y), folds, points)
    code = np.full(np.amax(points, axis=1) + 1, '.')
    code[tuple(zip(*points.T))] = '#'
    code = np.rot90(np.flip(code, axis=1))
    yield f'\n{'\n'.join([''.join(x) for x in code])}'

if __name__ == '__main__':
    aoc.run()
