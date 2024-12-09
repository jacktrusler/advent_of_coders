import aoc
from aoc.grid import Point
from collections import defaultdict
import itertools
from typing import Iterator


def parse_map(antenna_map: list[list[str]]) -> dict[str, set[Point]]:
    retval = defaultdict(set)
    for y, row in enumerate(antenna_map):
        for x, v in enumerate(row):
            if v != '.':
                retval[v].add(Point(x, y))
    return retval

def slope(a: Point, b: Point) -> tuple[int, int]:
    return b.x - a.x, b.y - a.y

def within(shape: Point, p: Point):
    return 0 <= p.x < shape.x and 0 <= p.y < shape.y

def antinodes(shape: Point, a: Point, b: Point) -> Iterator[Point]:
    _slope = slope(a, b)

    for antinode in (a - _slope, b + _slope):
        if within(shape, antinode):
            yield antinode

def resonant_antinodes(shape: Point, a: Point, b: Point) -> Iterator[Point]:
    _slope = slope(a, b)
    
    def _check(p: Point, slope: Point):
        while within(shape, p):
            yield p
            p += slope

    yield from _check(a, (-_slope[0], -_slope[1]))
    yield from _check(b, _slope)

@aoc.register(__file__)
def answers():
    antenna_map = aoc.read_grid()
    width, height = len(antenna_map[0]), len(antenna_map)
    antenna_map = parse_map(antenna_map)
    shape = Point(width, height)

    # Part One
    all_antinodes = set(an for v in antenna_map.values() for a, b in itertools.combinations(v, r=2) for an in antinodes(shape, a, b))
    yield len(all_antinodes)

    # Part Two
    all_antinodes = set(an for v in antenna_map.values() for a, b in itertools.combinations(v, r=2) for an in resonant_antinodes(shape, a, b))
    yield len(all_antinodes)
    
if __name__ == '__main__':
    aoc.run()
