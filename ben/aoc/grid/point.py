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
    
    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)
    
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
    p1 = Point(3,7)
    p2 = Point(1,2)
    print(p1+p2)

    print(p1.rotate())
    print(p1.distance(p2))
