import aoc
from aoc.grid import Point, KeyGrid, Line, LineSegment
import itertools
from typing import Iterator


class AntennaMap(KeyGrid):
    ignore = '.'

    def pairs(self) -> Iterator[tuple[Point, Point]]:
        yield from itertools.chain((a, b) for v in self.values() for a, b in itertools.combinations(v, r=2))

    def antinodes(self) -> set[Point]:
        def _antinodes(a: Point, b: Point) -> Iterator[Point]:
            line = LineSegment(a, b)
            possibilities = {line.prev(a), line.next(a), line.prev(b), line.next(b)}
            for antinode in possibilities - {a, b}:
                if self.binds(antinode):
                    yield antinode

        return set(p for a, b in self.pairs() for p in _antinodes(a, b))

    def resonant_antinodes(self) -> Iterator[Point]:
        def _antinodes(a: Point, b: Point) -> Iterator[Point]:
            line = Line(a, b)
            yield from (p for p in line.points(self.top_left.x, self.bottom_right.x) if self.binds(p))

        return set(p for a, b in self.pairs() for p in _antinodes(a, b))

@aoc.register(__file__)
def answers():
    antenna_map = AntennaMap(aoc.read_data())
    yield len(antenna_map.antinodes())
    yield len(antenna_map.resonant_antinodes())
    
if __name__ == '__main__':
    aoc.run()
