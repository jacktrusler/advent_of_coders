from __future__ import annotations
import aoc
from collections import defaultdict, deque
from enum import Enum
import functools
import re
from typing import Generator


class Lens(Enum):
    EMPTY = '.'
    FMIRROR = '/'
    BMIRROR = '\\'
    HSPLITTER = '-'
    VSPLITTER = '|'

def encounter(lens: Lens, dir: aoc.Direction) -> Generator[aoc.Direction]:
    match lens:
        case Lens.EMPTY: yield dir
        case Lens.FMIRROR: yield dir.rotate(1) if dir.vertical else dir.rotate(-1)
        case Lens.BMIRROR: yield dir.rotate(1) if dir.horizontal else dir.rotate(-1)
        case Lens.HSPLITTER: yield from (dir,) if dir.horizontal else (aoc.Direction.LEFT, aoc.Direction.RIGHT)
        case Lens.VSPLITTER: yield from (dir,) if dir.vertical else (aoc.Direction.UP, aoc.Direction.DOWN)

class Contraption:
    def __init__(self, layout: str):
        line_length = layout.index('\n') + 1
        def _per_match(layout: dict, m: re.Match):
            y, x = divmod(m.start(), line_length)
            key = m.group(0)
            layout[aoc.Point(x,y)] = Lens(key)
            return layout
        self.layout = functools.reduce(lambda l, m: _per_match(l, m), re.finditer(r'[-|\/\\]', layout), dict())
        self.height = layout.count('\n') + 1
        self.width = line_length - 1

    def __getitem__(self, point: aoc.Point) -> Lens:
        if point in self:
            try:
                return self.layout[point]
            except KeyError:
                return Lens.EMPTY
        raise KeyError

    def __contains__(self, point: aoc.Point) -> bool:
        return 0 <= point[0] < self.width and 0 <= point[1] < self.height

    def energize(self, entrance: aoc.Point, direction: aoc.Direction) -> int:
        energized = defaultdict(set)
        queue = deque([(entrance, direction)])

        while queue:
            p, dir = queue.popleft()
            try:
                val = self[p]
            except KeyError:
                continue

            if p in energized[dir]:
                continue
            energized[dir].add(p)

            for new_d in encounter(val, dir):
                queue.append((p.move(new_d), new_d))

        all_energized = set.union(*energized.values())
        return len(all_energized)
    
    def entrances(self) -> Generator[aoc.Point, aoc.Direction]:
        max_y = self.height - 1
        for x in range(self.width):
            yield (aoc.Point(x, 0), aoc.Direction.DOWN)
            yield (aoc.Point(x, max_y), aoc.Direction.UP)
        max_x = self.width - 1
        for y in range(self.height):
            yield (aoc.Point(0, y), aoc.Direction.RIGHT)
            yield (aoc.Point(max_x, y), aoc.Direction.LEFT)


@aoc.register(__file__)
def answers():
    contraption = Contraption(aoc.read_data())
    yield(contraption.energize(entrance=aoc.Point(0,0), direction=aoc.Direction.RIGHT))
    yield(max(contraption.energize(p, d) for p, d in contraption.entrances()))

if __name__ == '__main__':
    aoc.run()
