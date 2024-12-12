from __future__ import annotations
from aoc.grid import Point
from fractions import Fraction
from functools import cached_property
from typing import Iterator


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.slope: Fraction = Fraction((p2.y - p1.y), (p2.x - p1.x))
        self.y_intercept: int | Fraction = p1.y - (self.slope * p1.x)

    def __repr__(self):
        return f'Line(m={self.slope}, b={self.y_intercept})'
    
    def __str__(self):
        return f'Line(m={self.slope}, b={self.y_intercept})'
    
    def __eq__ (self, other: Line):
        return self.slope == other.slope and self.y_intercept == other.y_intercept
    
    def __and__(self, other: Line):
        return self.intersection(other)
    
    def __contains__(self, point: Point):
        return point == self.at_x(point.x)
    
    def at_x(self, x: int) -> Point:
        y = (self.slope * x) + self.y_intercept
        if y.denominator != 1: return None
        return Point(x, int(y))
    
    def at_y(self, y: int) -> Point:
        x = (y - self.y_intercept) // self.slope
        if x.denominator != 1: return None
        return Point(int(x), y)
    
    @cached_property
    def x_intercept(self) -> int | Fraction:
        return -self.y_intercept // self.slope
    
    def intersection(self, other: Line) -> Point | None:
        x = (other.y_intercept - self.y_intercept) // (self.slope - other.slope)
        y = (self.slope * x) + self.y_intercept
        return Point(x, y)
    
    def points(self, min_x: int, max_x: int) -> Iterator[Point]:
        x = min_x
        while x <= max_x:
            if (p := self.at_x(x)) is not None:
                yield p
                break
            x += 1

        slope_p = Point(self.slope.denominator, self.slope.numerator)
        while p.x <= max_x:
            p += slope_p
            yield p


class LineSegment:
    def __init__(self, start: Point, end: Point):
        self.start = Point(*start)
        self.end = Point(*end)

    def __repr__(self):
        return f'LineSegment({self.start}, {self.end})'
    
    def __str__(self):
        return f'[{self.start}, {self.end}]'
    
    def __len__(self):
        return int(self.distance)
    
    def __eq__ (self, other: LineSegment):
        return self.start == other.start and self.end == other.end
    
    def __and__(self, other: LineSegment):
        return self.intersection(other)
    
    def __contains__(self, point: Point):
        if point.x < self.min_x or point.x > self.max_x: return False
        if point.y < self.min_y or point.y > self.max_y: return False
        if (slope := self.slope) is None: return point.x == self.start.x
        if slope == 0: return point.y == self.start.y
        if (point.x - self.min_x) % slope.denominator != 0: return False
        if (point.y - self.min_y) % slope.numerator != 0: return False
        return True
    
    def at_x(self, x: int) -> Point:
        if (slope := self.slope) is None: return None
        if x < self.min_x or x > self.max_x: return None
        if x % slope.numerator != 0: return None
        y_intercept = self.start.y - (slope * self.start.x)
        y = (slope * x) + y_intercept
        return Point(x, y)
    
    def at_y(self, y: int) -> Point:
        if (slope := self.slope) is None: return None
        if y % slope.denominator != 0: return None
        if y < self.min_y or x > self.max_y: return None
        y_intercept = self.start.y - (slope * self.start.x)
        x = (y - y_intercept) // slope
        return Point(x, y)
    
    def next(self, p: Point) -> Point:
        if (slope := self.slope) is None:
            return p + Point(0, 1)
        return p + Point(slope.denominator, slope.numerator)
    
    def prev(self, p: Point) -> Point:
        if (slope := self.slope) is None:
            return p - Point(0, 1)
        return p - Point(slope.denominator, slope.numerator)
    
    @cached_property
    def slope(self) -> Fraction:
        try:
            return Fraction(self.end.y - self.start.y, self.end.x - self.start.x)
        except ZeroDivisionError:
            return None
    
    @cached_property
    def distance(self) -> float:
        return self.start.distance(self.end)
    
    @cached_property
    def min_x(self) -> int: return min(self.start.x, self.end.x)
    @cached_property
    def max_x(self) -> int: return max(self.start.x, self.end.x)
    @cached_property
    def min_y(self) -> int: return min(self.start.y, self.end.y)
    @cached_property
    def max_y(self) -> int: return max(self.start.y, self.end.y)
    
    def intersection(self, other: LineSegment) -> Point | None:
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
    

if __name__ == '__main__':
    from aoc import Point
    p1 = Point(0, 0)
    p2 = Point(1, 1)
    l1 = Line(p1, p2)
    p3 = Point(-4, 0)
    p4 = Point(-3, -1)
    l2 = Line(p3, p4)
    print(l1, l2)
    print(l1 & l2)

    l3 = Line(Point(0, 0), Point(2, 1))
    print(l3)
    for p in l3.points(-10, 10):
        print(p)


    ls1 = LineSegment(Point(-10, -10), Point(8, 8))
    ls2 = LineSegment(Point(-5, 2), Point(20, 2))
    print(ls1, ls2)
    print(ls1 & ls2)

    print(Point(0, 2) in ls2)
    print(Point(-8, 2) in ls2)