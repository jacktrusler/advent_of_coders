from __future__ import annotations
from collections import namedtuple
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aoc.grid.direction import Direction


RAW_POINT = tuple[int, int]
class Point(namedtuple('Point', ['x', 'y'])):
    def __repr__(self):
        return f'Point({self[0]}, {self[1]})'
    
    def __str__(self):
        return f'({self[0]}, {self[1]})'
    
    def __add__(self, other: Point | RAW_POINT) -> Point:
        return self.__class__(self[0] + other[0], self[1] + other[1])
    
    def __radd__(self, other: Point | RAW_POINT) -> Point:
        return self.__class__(self[0] + other[0], self[1] + other[1])
    
    def __sub__(self, other: Point | RAW_POINT) -> Point:
        return self.__class__(self[0] - other[0], self[1] - other[1])
    
    def __mul__(self, val: int) -> Point:
        return self.__class__(self.x * val, self.y * val)
    
    def __mod__(self, other: Point | RAW_POINT) -> Point:
        return self.__class__(self[0] % other[0], self[1] % other[1])
    
    def distance(self, other: Point | RAW_POINT) -> float:
        return math.hypot(*(self - other))
    
    def manhattan_distance(self, other: Point | RAW_POINT = (0, 0)) -> int:
        return abs(self[0] - other[0]) + abs(self[1] - other[1])
    
    def move(self, direction: Direction, n: int = 1) -> Point:
        return self + direction.movement * n
    

if __name__ == '__main__':
    import random
    i = 1000
    x = random.randint(0, i-1)

    import time
    def test_time(f, *args, **kwargs):
        start = time.perf_counter()
        ret = f(*args, **kwargs)
        end = time.perf_counter()
        print(f'Time elapsed {f}: {round((end - start) * 1000, 3)} ms')
        return ret
    
    print('--- Create ---')
    def create_tuple(n):
        return [(v,v) for v in range(n)]
    def creator(cls, n):
        return [cls(v, v) for v in range(n)]
    
    t_pts = test_time(create_tuple, i)
    nt_pts = test_time(creator, Point, i)

    print('--- Add ---')
    def add_em(l):
        return [p + p for p in l]
    def add_og(l):
        return [(p[0] + p[0], p[1] + [1]) for p in l]
    
    print(nt_pts[0])
    asdf = Point(1, 2)
    import aoc
    print(asdf.move(aoc.Direction.UP, 2))
    
    test_time(add_em, t_pts)
    test_time(add_em, nt_pts)
