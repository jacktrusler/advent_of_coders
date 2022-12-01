from __future__ import annotations
import aoc
from collections import Counter
import itertools
import re


class Line:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1, self.x2 = x1, x2
        self.y1, self.y2 = y1, y2

    @property
    def diagonal(self) -> bool:
        return not ((self.x1 == self.x2) or (self.y1 == self.y2))

    @property
    def points(self) -> set[tuple[int,int]]:
        if self.x1 == self.x2:
            step = 1 if self.y2 > self.y1 else -1
            return {(self.x1, y) for y in range(self.y1, self.y2+step, step)}
        elif self.y1 == self.y2:
            step = 1 if self.x2 > self.x1 else -1
            return {(x, self.y1) for x in range(self.x1, self.x2+step, step)}
        else:
            x_step = 1 if self.x2 > self.x1 else -1
            y_step = 1 if self.y2 > self.y1 else -1
            return set(zip(range(self.x1, self.x2+x_step, x_step), range(self.y1, self.y2+y_step, y_step)))

    @staticmethod
    def from_string(line_str: str) -> Line:
        args = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line_str).groups()
        return Line(*list(map(int, args)))


@aoc.register(__file__)
def answers():
    lines = [Line.from_string(line) for line in aoc.read_lines()]

    points = Counter(itertools.chain.from_iterable(line.points for line in lines if not line.diagonal))
    yield len({point for point, count in points.items() if count >= 2})

    points.update(Counter(itertools.chain.from_iterable(line.points for line in lines if line.diagonal)))
    yield len({point for point, count in points.items() if count >= 2})

if __name__ == '__main__':
    aoc.run()
