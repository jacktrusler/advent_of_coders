from __future__ import annotations
from aoc.grid.point import Point
import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import convolve
from typing import Generator, Iterable


ALL_ADJACENT = np.array([
    [1,1,1],
    [1,0,1],
    [1,1,1]
])
def count_adjacent(ar: NDArray, window=ALL_ADJACENT) -> NDArray:
    return convolve(ar, window, mode='constant')

def points(truth: NDArray[np.bool_]) -> Generator[Point]:
    yield from (Point(x[1], x[0]) for x in zip(*np.where(truth)))

def indexes(points: Iterable[Point]) -> tuple[list]:
    return tuple(list(x) for x in zip(*points))[::-1]
