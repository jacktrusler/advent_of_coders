from __future__ import annotations
from abc import ABC
from aoc.grid import Point
from aoc.utils.numpy import points
from dataclasses import dataclass, field
import numpy as np
from numpy.typing import NDArray
from typing import Iterable, TypeVar, Generic, Generator, Iterator


T = TypeVar('T')
INDEX = tuple[int, int] | Point
class Grid(Generic[T]):
    def __init__(self, data: Iterable[Iterable[T]]):
        self._data = tuple(tuple(x) for x in data)
        self.height = len(self._data[0])
        try:
            self.width = len(self._data[0])
        except IndexError:
            self.width = 0

    def __hash__(self):
        return hash(self._data)
    
    def __eq__(self, other: Grid):
        return self._data == other._data

    def __str__(self):
        return '\n'.join(str(x) for x in self._data)
    
    def __contains__(self, idx: INDEX) -> bool:
        return 0 <= idx[0] < self.width and 0 <= idx[1] < self.height
    
    def __getitem__(self, idx: INDEX) -> T:
        return self._data[idx[1]][idx[0]]
    
    def __iter__(self) -> Iterator[tuple[T]]:
        return iter(self._data)
    
    def rows(self) -> Generator[tuple[T]]:
        yield from self._data

    def columns(self) -> Generator[tuple[T]]:
        yield from zip(*self._data)

    def rotate(self, n: int = 1, clockwise: bool = True) -> Grid:
        n = n % 4 if clockwise else (4 - n) % 4
        match n:
            case 0:
                return Grid(self._data)
            case 1:
                return Grid(reversed(x) for x in zip(*self._data))
            case 2:
                return Grid(x[::-1] for x in self._data[::-1])
            case 3:
                return Grid(tuple(reversed(x) for x in zip(*self._data[::-1]))[::-1])
        

        


class _Grid(ABC):
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

        
    

class TestGrid(_Grid):
    test = lambda x: x > 8

if __name__ == '__main__':
    # g = TestGrid([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
    # print(g)
    # print(g.test)

    grid: Grid[int] = Grid([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
    for c in grid.columns():
        print(c)
