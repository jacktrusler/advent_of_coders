from __future__ import annotations
from abc import ABC, ABCMeta
from aoc.grid import Point
from collections import Counter, defaultdict
from collections.abc import Iterable
from functools import cached_property
import itertools
import re
from typing import Iterable, TypeVar, Generic, Generator, Iterator, Type


class PostInitCaller(type):
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.__post_init__()
        return obj
BaseGridMeta = type('BaseGridMeta', (ABCMeta, PostInitCaller), {})


T = TypeVar('T')
class BaseGrid(Generic[T]):
    __metaclass__ = BaseGridMeta

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def __post_init__(self): pass

    def binds(self, idx: tuple[int, int] | Point) -> bool:
        return 0 <= idx[0] < self.width and 0 <= idx[1] < self.height
    
    @cached_property
    def top_left(self) -> Point: return Point(0, 0)
    @cached_property
    def top_right(self) -> Point: return Point(self.width-1, 0)
    @cached_property
    def bottom_left(self) -> Point: return Point(0, self.height-1)
    @cached_property
    def bottom_right(self) -> Point: return Point(self.width-1, self.height-1)


class Grid(BaseGrid, Generic[T]):
    def __init__(self, data: Iterable[Iterable[T]], dtype: Type = None):
        self.__data = list(list(dtype(v) for v in r) for r in data) if dtype else list(list(v for v in r) for r in data)
        self.dtype = dtype

        height = len(self.__data)
        width = len(self.__data[0]) if height else 0
        super().__init__(width, height)
        if height == 0: return

        # Validate data
        if any(len(r) != width for r in self.__data): raise ValueError(f'Invalid grid dimensions')

    def __hash__(self): return hash(self.__data)
    def __eq__(self, other: Grid): return self.__data == other.__data
    def __str__(self): return '\n'.join(str(x) for x in self.__data)
    def __repr__(self): return f'{self.__class__}()'
    def __iter__(self) -> Iterator[tuple[T]]: return iter(self.__data)
    
    def __contains__(self, value: T) -> bool:
        if self.dtype and not isinstance(value, self.dtype): return False
        return any(value in row for row in self.__data)
    
    def __getitem__(self, idx) -> T:
        match idx:
            case tuple() if len(idx) == 2 and not isinstance(idx[0], tuple):
                first = idx[0]
                if isinstance(first, slice) and len(idx) == 2:
                    return self.slice(*idx)
                if isinstance(first, int) and len(idx) <= 2:
                    return self.__data[idx[1]][idx[0]]
            case int(): return self.__data[idx]
            case slice(): return self.slice(idx)
            case Point(): return self.__data[idx.y][idx.x]
            case tuple() | list() | set(): return tuple(self[x] for x in idx)
        raise TypeError(f'Invalid index: {idx}')
    
    def __setitem__(self, idx, value: T):
        if self.dtype and not isinstance(value, self.dtype):
            raise TypeError(f'Incompatible dtype for Grid[{self.dtype.__name__}]: {value}')
        
        match idx:
            case tuple() if len(idx) == 2:
                first = idx[0]
                if isinstance(first, slice) and len(idx) == 2:
                    self.__set_slice(value, *idx)
                if isinstance(first, int) and len(idx) <= 2:
                    self.__data[idx[1]][idx[0]] = value
            case slice(): self.__set_slice(value, idx)
            case Point(): self.__data[idx.y][idx.x] = value
            case tuple() | list() | set():
                for p in idx:
                    self[p] = value
            case _: raise TypeError(f'Invalid index: {idx}')
    
    def values(self) -> Generator[T]: yield from (v for r in self.__data for v in r)
    def rows(self) -> Generator[tuple[T]]: yield from self.__data
    def columns(self) -> Generator[tuple[T]]: yield from zip(*self.__data)

    def __set_slice(self, value: T, x: slice = None, y: slice = None):
        def _slice_to_range(s: slice, default: int) -> range:
            if s is None:
                return range(default)
            return range(s.start or 0, s.stop or default, s.step or 1)
        x_range, y_range = _slice_to_range(x, self.width), _slice_to_range(y, self.height)
        
        for _y in y_range:
            for _x in x_range:
                self.__data[_y][_x] = value
    
    def slice(self, x: slice = None, y: slice = None) -> Grid:
        data = self.__data[y] if y else self.__data
        if x:
            return Grid((row[x] for row in data), dtype=self.dtype)
        return Grid(data, dtype=self.dtype)

    def rotate(self, n: int = 1, clockwise: bool = True) -> Grid:
        n = n % 4 if clockwise else (4 - n) % 4
        match n:
            case 0: data = self.__data
            case 1: data = (zip(*self.__data[::-1]))
            case 2: data = (x[::-1] for x in self.__data[::-1])
            case 3: data = (zip(*(x[::-1] for x in self.__data)))
        return Grid(data, dtype=self.dtype)
            
    def flip(self, horizontal: bool = True) -> Grid:
        data = tuple(x[::-1] for x in self.__data) if horizontal else self.__data[::-1]
        return Grid(data, dtype=self.dtype)
        
    def count(self, value: T | Iterable[T]) -> int:
        if self.dtype and not isinstance(value, self.dtype): return 0
        if isinstance(value, (tuple, list, set)):
            c = Counter(itertools.chain(*self.__data))
            return sum(c[v] for v in value)
        else:
            return sum(row.count(value) for row in self.__data)
        

class KeyGrid(BaseGrid, Generic[T], ABC):
    def __init__(self, data: str):
        self.__points: dict[str, set[Point]] = defaultdict(set)
        members = set(vars(self.__class__)) - set(vars(KeyGrid))
        targets = dict()
        for x in members:
            target = getattr(self.__class__, x)
            targets[target] = x
            if isinstance(target, str):
                setattr(self, x, lambda: self.__points[x])

        line_length = data.index('\n') + 1
        regex = rf'[{"".join(targets.keys())}]'
        def _per_match(m: re.Match):
            y, x = divmod(m.start(), line_length)
            key = m.group(0)
            self.__points[key].add(Point(x, y))
        [_per_match(m) for m in re.finditer(regex, data)]
        print(self.__points)
        two = 2
    

class TestGrid(KeyGrid):
    import numpy as np

    test = r'\^'

if __name__ == '__main__':
    import time
    def test_time(f, *args, **kwargs):
        start = time.perf_counter()
        ret = f(*args, **kwargs)
        end = time.perf_counter()
        print(f'Time elapsed {f}: {round((end - start) * 1000, 3)} ms')
        return ret

    import numpy as np
    def _np(i):
        return np.array([[x+(i2) for x in range(i)] for i2 in range(i)])
    def _str_np(i):
        return np.array([['#' for x in range(i)] for i2 in range(i)])
    
    def _g(i):
        return Grid((x+(i2) for x in range(i)) for i2 in range(i))
    def _str_g(i):
        return Grid((('#' for x in range(i)) for i2 in range(i)), dtype=str)
    
    print('-- Create int --')
    i = 50
    iar = test_time(_np, i=i)
    igr = test_time(_g,  i=i)

    print('-- Create str --')
    ar = test_time(_str_np, i=i)
    gr = test_time(_str_g, i=i)

    print('-- Rotate --')
    n = 3
    test_time(np.rot90, ar, -n)
    test_time(gr.rotate, n)

    # print('-- Flip --')
    # test_time(np.flip, ar, 0)
    # test_time(gr.flip)

    # print('-- Multi slice --')
    # fn = lambda x: x[3:5, 7:10]
    # test_time(fn, ar)
    # test_time(fn, gr)

    # print('-- Index tuple --')
    # fn = lambda x: x[(1, 1)]
    # test_time(fn, ar)
    # test_time(fn, gr)

    # print('-- Single slice --')
    # fn = lambda x: x[3:5]
    # test_time(fn, ar)
    # test_time(fn, gr)

    # print('-- Contains int --')
    # fn = lambda x: 28 in x
    # print(test_time(fn, iar))
    # print(test_time(fn, igr))

    # print('-- Contains str --')
    # fn = lambda x: '#' in x
    # print(test_time(fn, ar))
    # print(test_time(fn, gr))

    # print('-- Count int --')
    # fn = lambda ar, x: np.count_nonzero(ar == x)
    # print(test_time(fn, iar, 14))
    # print(test_time(igr.count, 14))

    # print('-- Count str --')
    # print(test_time(fn, ar, '#'))
    # print(test_time(gr.count, '#'))

    # def fn(a, v):
    #     a[2:10, 2:10] = v
    # print('-- Set int --')
    # test_time(fn, iar, 2000)
    # test_time(fn, igr, 2000)
    # print('-- Set str --')
    # test_time(fn, ar, '!')
    # test_time(fn, gr, '!')

    test_str = '...^\n.^..\n^^..\n....'
    kg = TestGrid(test_str)
    print(kg)
    print(kg.test)


    

    # # g = TestGrid([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
    # # print(g)
    # # print(g.test)

    # grid: Grid[int] = Grid([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
    # for c in grid.columns():
    #     print(c)
