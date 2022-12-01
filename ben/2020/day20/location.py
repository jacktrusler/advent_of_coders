from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    ABOVE = 0
    RIGHT = 1
    BELOW = 2
    LEFT = 3

    def __add__(self, value: int) -> Direction:
        v = value.value if isinstance(value, Direction) else value
        return Direction((self.value + v) % 4)

    def __sub__(self, value: int) -> Direction:
        v = value.value if isinstance(value, Direction) else value
        return Direction((self.value - v) % 4)
        

@dataclass
class Location:
    x: int
    y: int

    def __str__(self):
        return f'{self.x}, {self.y}'

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other: Location) -> Location:
        return Location(self.x + other.x, self.y + other.y)

    def move(self, dir: Direction) -> Location:
        match dir:
            case Direction.ABOVE: return Location(self.x, self.y - 1)
            case Direction.RIGHT: return Location(self.x + 1, self.y)
            case Direction.BELOW: return Location(self.x, self.y + 1)
            case Direction.LEFT:  return Location(self.x - 1, self.y)
