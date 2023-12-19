from __future__ import annotations
from aoc.grid.point import Point
from aoc.grid.direction import Direction
from typing import Iterable, Type, Generator


def pairwise(iterable: Iterable):
    a = iter(iterable)
    return zip(a, a)

def adjacent_points(point: Point, dir_type: Type[Direction] = Direction, include_dir: bool = False) -> Generator[Direction, Point]:
    if include_dir:
        yield from ((d, point + d.movement) for d in dir_type)
    else:
        yield from (point + d.movement for d in dir_type)
