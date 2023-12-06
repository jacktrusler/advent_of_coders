from aoc.grid import Point
import numpy as np
from numpy.typing import NDArray
from typing import Iterable


class Grid:
    def __init__(self, data: Iterable[Iterable[any]]):
        self._data = np.array(data)

    def __repr__(self) -> str:
        return f'{self._data}'
    
    def __getitem__(self, point: Point):
        return self._data[point.y, point.x]
    
    def shape(self) -> tuple[int, int]:
        return self._data.shape[::-1]


if __name__ == '__main__':
    g = Grid([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
    print(g)

    print(g.shape())
    print(g._data[(2,1)])
