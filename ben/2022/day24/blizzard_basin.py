from __future__ import annotations
import aoc
from dataclasses import dataclass
from enum import Enum
from functools import cache
import math
import numpy as np
from numpy.typing import NDArray
from typing import Generator


def locations(truth: NDArray) -> Generator[Location]:
    yield from (Location(x[1], x[0]) for x in zip(*np.where(truth)))


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


@dataclass
class Location:
    x: int
    y: int

    def __getitem__(self, idx: int) -> int:
        match idx:
            case 0: return self.x
            case 1: return self.y
            case _: raise IndexError

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other) -> Location:
        return Location(self.x + other[0], self.y + other[1])
    
    def move(self, dir: Direction, amt: int = 1) -> Location:
        match dir:
            case Direction.UP: return self + (0, -amt)
            case Direction.DOWN: return self + (0, amt)
            case Direction.LEFT: return self + (-amt, 0)
            case Direction.RIGHT: return self + (amt, 0)
    

class Blizzards:
    BLIZZARD_MAP = {Direction.UP: '^', Direction.RIGHT: '>', Direction.DOWN: 'v', Direction.LEFT: '<'}

    def __init__(self, grid):
        w, h = len(grid[0]) - 2, len(grid) - 2
        self.cycle = abs(w * h) // math.gcd(w, h)
        start = {d: set(locations(grid == self.BLIZZARD_MAP[d])) for d in Direction}

        self._v_cycle = []
        for i in range(h):
            locs = set.union(*({x.move(d, i) for x in start[d]} for d in (Direction.UP, Direction.DOWN)))
            self._v_cycle.append({Location(loc.x, (loc.y - 1) % h + 1) for loc in locs})

        self._h_cycle = []
        for i in range(w):
            locs = set.union(*({x.move(d, i) for x in start[d]} for d in (Direction.LEFT, Direction.RIGHT)))
            self._h_cycle.append({Location((loc.x - 1) % w + 1, loc.y) for loc in locs})

    @cache
    def _at_cycle(self, time: int) -> set[Location]:
        return self._h_cycle[time % len(self._h_cycle)] | self._v_cycle[time % len(self._v_cycle)]

    def at(self, time: int) -> set[Location]:
        return self._at_cycle(time % self.cycle)


class Valley:
    def __init__(self, grid: NDArray):
        self.shape = (len(grid[0]), len(grid[:, 0]))
        self.walls = set(locations(grid == '#'))
        self.entrance = Location(np.where(grid[0] == '.')[0][0], 0)
        self.exit = Location(np.where(grid[-1] == '.')[0][0], len(grid)-1)
        self.blizzards = Blizzards(grid)

    def __contains__(self, loc: Location) -> bool:
        return loc not in self.walls and 0 <= loc.x < self.shape[0] and 0 <= loc.y < self.shape[1]
    
    @cache
    def neighbors(self, loc: Location) -> set[Location]:
        return {x for x in {loc.move(d) for d in Direction} if x in self}

    def adjacent(self, locs: set[Location]) -> set[Location]:
        return set.union(*(self.neighbors(x) for x in locs))
    
    def path_to(self, start: Location, end: Location, time: int = 0) -> int:
        state = ({start}, time)

        while end not in state[0]:
            next_time = state[1] + 1
            next_blizzard = self.blizzards.at(next_time)
            possible_expeditions = self.adjacent(state[0])

            possible_locs = (possible_expeditions | state[0]) - next_blizzard
            state = (possible_locs, next_time)
        return state[1]


@aoc.register(__file__)
def answers():
    valley = Valley(np.array(aoc.read_grid()))

    time = valley.path_to(start=valley.entrance, end=valley.exit)
    yield time

    time = valley.path_to(start=valley.exit, end=valley.entrance, time=time)
    yield valley.path_to(start=valley.entrance, end=valley.exit, time=time)

if __name__ == '__main__':
    aoc.run(profile=True)
