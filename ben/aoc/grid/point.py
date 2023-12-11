from __future__ import annotations
from dataclasses import dataclass
import math


@dataclass()
class Point:
    x: int
    y: int

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'
    
    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, idx: int) -> int:
        match idx:
            case 0: return self.x
            case 1: return self.y
            case _: raise IndexError

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __add__(self, other: Point) -> Point:
        return Point(self.x + other[0], self.y + other[1])
    
    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)
    
    def __mul__(self, val: int) -> Point:
        return Point(self.x * val, self.y * val)
    
    def __mod__(self, other: Point) -> Point:
        return Point(self.x % other.x, self.y % other.y)
    
    def __eq__(self, other: Point) -> bool:
        return self.x == other[0] and self.y == other[1]
    
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

    # def adjacent(self, dirs: Type[Direction] = Direction) -> Generator[tuple[Direction, Point]]:
    #     yield from ((d, self + d.movement) for d in dirs)
