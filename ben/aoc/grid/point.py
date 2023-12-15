from __future__ import annotations
from collections import namedtuple
from dataclasses import dataclass
import math


@dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'
    
    def __iter__(self):
        yield from (self.x, self.y)

    def __getitem__(self, idx: int) -> int:
        match idx:
            case 0: return self.x
            case 1: return self.y
            case _: raise IndexError
    
    def __add__(self, other: Point) -> Point:
        return Point(self.x + other[0], self.y + other[1])
    
    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, val: int) -> Point:
        return Point(self.x * val, self.y * val)
    
    def __mod__(self, other: Point) -> Point:
        return Point(self.x % other.x, self.y % other.y)
    
    def __eq__(self, other: Point) -> bool:
        try:
            return self.x == other[0] and self.y == other[1]
        except TypeError:
            return False
    
    def distance(self, other: Point) -> float:
        return math.hypot(*(self - other))
    
    def manhattan_distance(self, other: Point = None) -> int:
        other = Point(0, 0) if other is None else other
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def rotate(self, n: int = 1, clockwise: bool = True) -> Point:
        n = n % 4 if clockwise else 4 - (n % 4)
        match n:
            case 0: return Point(self.x, self.y)
            case 1: return Point(self.y, -self.x)
            case 2: return Point(-self.x, -self.y)
            case 3: return Point(-self.y, self.x)

if __name__ == '__main__':
    import random
    i = 1000000
    x = random.randint(0, i-1)

    import time
    start = time.perf_counter()
    points = {Point(i, i): i for i in range(i)}
    p = points[Point(x, x)]
    end = time.perf_counter()
    print(f'Time elapsed: {round((end - start) * 1000, 3)} ms')

    start = time.perf_counter()
    points = {(i, i): i for i in range(i)}
    p = points[(x, x)]
    end = time.perf_counter()
    print(f'Time elapsed: {round((end - start) * 1000, 3)} ms')

    from collections import namedtuple
    Point2 = namedtuple('Point2', 'x y')
    start = time.perf_counter()
    points = {Point2(i, i): i for i in range(i)}
    p = points[(x, x)]
    end = time.perf_counter()
    print(f'Time elapsed: {round((end - start) * 1000, 3)} ms')

    Point3 = tuple[int, int]
    start = time.perf_counter()
    points = {Point3((i, i)): i for i in range(i)}
    p = points[(x, x)]
    end = time.perf_counter()
    print(f'Time elapsed: {round((end - start) * 1000, 3)} ms')
