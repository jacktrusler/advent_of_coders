from __future__ import annotations
from aoc.grid.point import Point
from enum import Enum


class Direction(Enum):
    UP = 1, 0, (0, -1)
    RIGHT = 2, 90, (1, 0)
    DOWN = 3, 180, (0, 1)
    LEFT = 4, 270, (-1, 0)

    def __new__(cls, *values):
        obj = object.__new__(cls)
        for other_val in values[1:]:
            cls._value2member_map_[other_val] = obj
        obj._value_ = values[0]
        obj._values = values
        return obj

    @property
    def degree(self) -> int:
        return self._values[1]
    
    @property
    def movement(self) -> Point:
        return self._values[2]
    
    def rotate(self, n: int = 1, clockwise: bool = True) -> Direction:
        rotated = self.value + (n if clockwise else -n)
        return Direction((rotated-1) % 4 + 1)
    
    @property
    def vertical(self) -> bool:
        return self in (Direction.UP, Direction.DOWN)
    
    @property
    def horizontal(self) -> bool:
        return self in (Direction.LEFT, Direction.RIGHT)
    
if __name__ == '__main__':
    d = Direction.RIGHT
    print(d.rotate(1))
    print(d.rotate(-1))
