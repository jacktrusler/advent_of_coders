from abc import ABC
from aoc.grid import Point
from aoc.utils.numpy import points
import numpy as np
from numpy.typing import NDArray
from typing import Iterable


class Grid(ABC):
    def __init__(self, data: Iterable[Iterable[any]]):
        grid = np.array(data)
        self.width = grid.shape[1]
        self.height = grid.shape[0]
        
        _members = set(vars(self.__class__)) - set(vars(Grid))
        for x in _members:
            method = getattr(self.__class__, x)
            if callable(method):
                truth = method(grid)
                setattr(self, x, set(points(truth)))
        self._setup(grid)

    def _setup(self, grid: NDArray):
        pass

        
    

class TestGrid(Grid):
    test = lambda x: x > 8

if __name__ == '__main__':
    g = TestGrid([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
    print(g)
    print(g.test)
