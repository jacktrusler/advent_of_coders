from __future__ import annotations
from abc import ABC
import aoc
from dataclasses import dataclass, field
from itertools import cycle
from typing import Type


class CollisionError(Exception):
    pass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point | tuple[int, int]) -> Point:
        try:
            return Point(self.x + other.x, self.y + other.y)
        except AttributeError:
            return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other: Point | tuple[int, int]) -> Point:
        try:
            return Point(self.x - other.x, self.y - other.y)
        except AttributeError:
            return Point(self.x - other[0], self.y - other[1])


@dataclass
class Map:
    width: int
    height: int = field(default=0, init=False)
    columns: dict[int, set[int]] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self):
        self.columns = {x: {0} for x in range(self.width)}

    def relative_y(self) -> tuple[int]:
        max_ys = tuple(max(y) for y in self.columns.values())
        return tuple(self.height - y for y in max_ys)

    def place(self, rock: Rock):
        [self.columns[p.x].add(p.y) for p in rock.points]
        self.height = max(self.height, max((p.y for p in rock.points)))
        self.columns = {x: set(filter(lambda n: n >= (self.height - 100), y)) for x, y in self.columns.items()}

    def __and__(self, other: Rock | set[Point]):
        points = other if not isinstance(other, Rock) else other.points
        return any(p.y in self.columns[p.x] for p in points)


@dataclass(eq=True, frozen=True)
class MapState:
    rock_type: Type[Rock]
    gas_index: int
    height: int = field(compare=False)
    relative_y: tuple[int]
    

class Rock(ABC):
    SHAPE = None

    def __init__(self, *, points: set[Point] = None, bottom_left: Point = None):
        assert(self.SHAPE is not None)
        if not ((points is None) ^ (bottom_left is None)):
            raise AttributeError

        try:
            self.points = {bottom_left + x for x in self.SHAPE}
        except TypeError:
            self.points = points
    
    def shift(self, map: Map, dir: str) -> Rock:
        shift_mod = 1 if dir == '>' else -1
        new_points = {p + (shift_mod, 0) for p in self.points}
        if any(p.x < 0 or p.x >= map.width for p in new_points):
            raise CollisionError
        if map & new_points:
            raise CollisionError
        return self.__class__(points=new_points)

    def fall(self, map: Map) -> Rock:
        new_points = {p - (0, 1) for p in self.points}
        if any(p.y < 0 for p in new_points):
            raise CollisionError
        if map & new_points:
            raise CollisionError
        return self.__class__(points=new_points)

class HorizontalRock(Rock):
    SHAPE = ((0, 0), (1, 0), (2, 0), (3, 0))

class PlusRock(Rock):
    SHAPE = ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2))

class LRock(Rock):
    SHAPE = ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))

class VerticalRock(Rock):
    SHAPE = ((0, 0), (0, 1), (0, 2), (0, 3))

class SquareRock(Rock):
    SHAPE = ((0, 0), (1, 0), (0, 1), (1, 1))


@aoc.register(__file__)
def answers():
    gas_pattern = list(aoc.read_data())
    gas_cycle = cycle(enumerate(gas_pattern))
    rock_cycle = cycle([
        HorizontalRock, PlusRock, LRock, VerticalRock, SquareRock
    ])

    rock_map = Map(width=7)
    states = []
    gas_i, i = 0, 0
    while True:
        new_rock = next(rock_cycle)(bottom_left=Point(x=2, y=rock_map.height + 4))

        new_state = MapState(
            rock_type=type(new_rock),
            gas_index = gas_i,
            height=rock_map.height,
            relative_y=rock_map.relative_y()
        )
        if new_state in states:
            start_i = states.index(new_state)
            end_i = i
            break
        states.append(new_state)
        while True:
            try:
                gas_i, next_gas = next(gas_cycle)
                new_rock = new_rock.shift(rock_map, next_gas)
            except CollisionError:
                pass

            try:
                new_rock = new_rock.fall(rock_map)
            except CollisionError:
                rock_map.place(new_rock)
                break
        i += 1

    def height(rock_count: int):
        cycle_len = i - start_i
        cycle_start = states[start_i]
        base_height = cycle_start.height
        cycle_height_gain = new_state.height - base_height
        num_cycles, remainder = divmod(rock_count - start_i, cycle_len)
        return cycle_height_gain * num_cycles + states[start_i + remainder].height
        
    yield height(2022)
    yield height(1_000_000_000_000)

if __name__ == '__main__':
    aoc.run()
