from __future__ import annotations
import aoc
from dataclasses import dataclass, field
import itertools
import re


Point = tuple[int, int]

def dist(p1: Point, p2: Point) -> int:
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

@dataclass
class Sensor:
    loc: Point
    closest_beacon: Point = field(repr=False)
    range: int = field(init=False, default=0)

    def __post_init__(self):
        self.range = dist(self.loc, self.closest_beacon)

    def points(self) -> set[Point]:
        return {self.loc, self.closest_beacon}

    def cross_row(self, y: int) -> tuple[int, int]:
        dist_from_row = dist(self.loc, (self.loc[0], y))
        if (_range := self.range - dist_from_row) < 0:
            return None
        return self.loc[0] - _range, self.loc[0] + _range

    def __contains__(self, p: Point) -> bool:
        return dist(self.loc, p) <= self.range
    
    @staticmethod
    def from_string(sensor_str: str) -> Sensor:
        m = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', sensor_str).groups()
        return Sensor(
            loc=(int(m[0]), int(m[1])),
            closest_beacon=(int(m[2]), int(m[3]))
        )

def reduce_ranges(ranges: set[tuple]) -> set[tuple]:
    for r1, r2 in itertools.combinations(ranges, 2):
        # No overlap
        if r1[1] < r2[0] or r2[1] < r1[0]:
            continue
        
        if r1[0] <= r2[0] and r1[1] >= r2[1]:
            ranges.remove(r2)
        elif r2[0] <= r1[0] and r2[1] >= r1[1]:
            ranges.remove(r1)
        else:
            ranges = (ranges - {r1, r2}) | {(min(r1[0], r2[0]), max(r1[1], r2[1]))}
        return reduce_ranges(ranges)
    return ranges

def within_ranges(ranges: set[tuple], x: int) -> bool:
    for low, high in ranges:
        if low <= x <= high:
            return True
    return False


@aoc.register(__file__)
def answers():
    data = 'data'
    sensors = [Sensor.from_string(line) for line in aoc.read_lines(data)]

    row = 10 if data == 'small' else 2_000_000
    ranges = set(filter(lambda x: x is not None, [s.cross_row(row) for s in sensors]))
    ranges = reduce_ranges(ranges)
    occupied = set.union(*[s.points() for s in sensors])
    occupied = [x for x in occupied if x[1] == row and within_ranges(ranges, x[0])]
    range_len = sum([r[1] - r[0] + 1 for r in ranges])
    yield range_len - len(occupied)
    
    xy_min = 0
    xy_max = 20 if data == 'small' else 4_000_000
    ul = { -s.loc[0] + s.loc[1] + s.range + 1 for s in sensors }
    lr = { -s.loc[0] + s.loc[1] - s.range - 1 for s in sensors }
    ur = { s.loc[0] + s.loc[1] + s.range + 1 for s in sensors }
    ll = { s.loc[0] + s.loc[1] - s.range - 1 for s in sensors }
    for pb, nb in itertools.product( ul & lr, ur & ll ):
        x = ( nb - pb ) // 2
        y = x + pb

        if not (xy_min <= x <= xy_max and xy_min <= y <= xy_max):
            continue
        if any([(x, y) in s for s in sensors]):
            continue
        yield x * 4_000_000 + y


if __name__ == '__main__':
    aoc.run()
