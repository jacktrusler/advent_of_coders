from __future__ import annotations
from aoc.grid import Point
from dataclasses import dataclass
import math


@dataclass
class Line:
    def __init__(self, start: Point, end: Point):
        self.start = Point(*start)
        self.end = Point(*end)

    def __repr__(self):
        return f'Line({self.start}, {self.end})'
    
    def __str__(self):
        return f'({self.start}, {self.end})'
    
    def __len__(self):
        return int(self.distance)
    
    def __eq__ (self, other: Line):
        return self.start == other.start and self.end == other.end
    
    def __and__(self, other: Line):
        return self.intersection(other)
    
    def __contains__(self, point: Point):
        raise NotImplementedError("This doesn't work yet")
    
    @property
    def distance(self) -> float:
        return math.sqrt((self.end.x - self.start.x) ^ 2 + (self.end.y - self.start.y) ^ 2)
    
    def intersection(self, other: Line) -> Point | None:
        x1, x2, x3, x4 = self.start.x, self.end.x, other.start.x, other.end.x
        y1, y2, y3, y4 = self.start.y, self.end.y, other.start.y, other.end.y
        
        cross_product = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
        if cross_product == 0: # parallel
            return None
        ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / cross_product
        if ua < 0 or ua > 1: # out of range
            return None
        ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / cross_product
        if ub < 0 or ub > 1: # out of range
            return None
        
        x = x1 + ua * (x2-x1)
        y = y1 + ua * (y2-y1)
        return Point(int(x), int(y))
    

class OrthogonalLine(Line):
    def __contains__(self, point: Point):
        if (self.start.x == self.end.x):
            return point.x == self.start.x and min(self.start.y, self.end.y) < point.y < max(self.start.y, self.end.y)
        return point.y == self.start.y and min(self.start.x, self.end.x) < point.x < max(self.start.x, self.end.x)

    @property
    def distance(self) -> int:
        return abs(self.start.y - self.end.y) if self.start.x == self.end.x else abs(self.start.x - self.end.x)
    
    def intersection(self, other: Line) -> Point | None:
        x1, x2, x3, x4 = self.start.x, self.end.x, other.start.x, other.end.x
        y1, y2, y3, y4 = self.start.y, self.end.y, other.start.y, other.end.y

        if max(x1, x2) < min(x3, x4) or min(x1, x2) > max(x3, x4) or max(y1, y2) < min(y3, y4) or min(y1, y2) > max(y3, y4):
            return None

        if (x1 == x2 and x3 != x4):
            return Point(self.start.x, other.start.y)
        elif (y1 == y2 and y3 != y4):
            return Point(other.start.x, self.start.y)
        return None
    

if __name__ == '__main__':
    from aoc import Point
    a = OrthogonalLine((0, 3), (0, -3))
    b = OrthogonalLine((1, 1), (-5, 1))
    print(a.intersection(b))
    print(a & b)

    p1 = Point(0, 2)
    p2 = Point(1, 2)
    print(p1 in a)
    print(p2 in a)
        