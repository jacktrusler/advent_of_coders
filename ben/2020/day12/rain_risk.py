from __future__ import annotations
from abc import ABC, abstractmethod
import aoc
from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class Direction(Enum):
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270

    def __str__(self):
        return self.name[0]

    def __add__(self, deg):
        return Direction((self.value + deg) % 360)

    def __sub__(self, deg):
        return Direction((self.value - deg) % 360)

@dataclass
class Location:
    x: int = 0
    y: int = 0

    def __repr__(self):
        return f'Location({self.x}, {self.y})'

    def __add__(self, other: Location):
        return Location(x = self.x + other.x, y = self.y + other.y)

    def __sub__(self, other: Location):
        return Location(x = self.x - other.x, y = self.y - other.y)

    def __mul__(self, val: int):
        return Location(self.x * val, self.y * val)

    def rotate(self, deg: int, clockwise: bool = True) -> Location:
        if (deg == 90 and clockwise) or (deg == 270 and not clockwise):
            return Location(self.y, -self.x)
        elif (deg == 180):
            return Location(-self.x, -self.y)
        elif (deg == 270 and clockwise) or (deg == 90 and not clockwise):
            return Location(-self.y, self.x)
        raise ValueError(f'Invalid angle: {deg}')

    def manhattan_dist(self) -> int:
        return abs(self.x) + abs(self.y)

@dataclass(kw_only=True)
class Ferry(ABC):
    loc: Location = Location()

    def move(self, commands: str | Iterable[str]) -> Ferry:
        commands = [commands] if isinstance(commands, str) else commands
        [self._move(cmd[0], int(cmd[1:])) for cmd in commands]
        return self

    @abstractmethod
    def _move(self, cmd: str, val: int):
        pass

@dataclass
class CardinalFerry(Ferry):
    direction: Direction

    def _move(self, cmd, val):
        match cmd:
            case 'N': self.loc += Location(0, val)
            case 'E': self.loc += Location(val, 0)
            case 'S': self.loc += Location(0, -val)
            case 'W': self.loc += Location(-val, 0)
            case 'L': self.direction -= val
            case 'R': self.direction += val
            case 'F': self._move(str(self.direction), val)

@dataclass
class RelativeFerry(Ferry):
    waypoint: Location

    def _move(self, cmd, val):
        match cmd:
            case 'N': self.waypoint += Location(0, val)
            case 'E': self.waypoint += Location(val, 0)
            case 'S': self.waypoint += Location(0, -val)
            case 'W': self.waypoint += Location(-val, 0)
            case 'L': self.waypoint = self.waypoint.rotate(val, clockwise=False)
            case 'R': self.waypoint = self.waypoint.rotate(val, clockwise=True)
            case 'F': self.loc += self.waypoint * val


@aoc.register(__file__)
def answers():
    commands = aoc.read_lines()

    ferry1 = CardinalFerry(direction=Direction.EAST)
    ferry1 = ferry1.move(commands)
    yield ferry1.loc.manhattan_dist()

    ferry2 = RelativeFerry(waypoint=Location(10, 1))
    ferry2 = ferry2.move(commands)
    yield ferry2.loc.manhattan_dist()

if __name__ == '__main__':
    aoc.run()
