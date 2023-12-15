from __future__ import annotations
import aoc
import functools
import itertools


def tilt(grid: aoc.Grid[str]) -> aoc.Grid[str]:
    def _tilt(line: str) -> str:
        groups = []
        for group in line.split('#'):
            groups.append(''.join(sorted(group)))
        return '#'.join(groups)
    return aoc.Grid(tuple(_tilt(''.join(x))) for x in grid)

def load(grid: aoc.Grid[str]) -> int:
    def _load(line: str) -> int:
        return sum(i for i, x in enumerate(line, 1) if x == 'O')
    return sum(_load(''.join(x)) for x in grid)

def cycle(grid: aoc.Grid[str]) -> aoc.Grid[str]:
    return functools.reduce(lambda g, _: tilt(g).rotate(), range(4), grid)


@aoc.register(__file__)
def answers():
    grid = aoc.Grid(aoc.read_grid()).rotate()
    yield load(tilt(grid))

    visited = list()
    for i in itertools.count():
        if grid in visited:
            loop_start = visited.index(grid)
            loop_cycles = i - loop_start
            break
        visited.append(grid)
        grid = cycle(grid)

    total_cycles = 1000000000
    loop = visited[loop_start:i]
    loop_x = (total_cycles - loop_start) % loop_cycles
    yield load(loop[loop_x])

if __name__ == '__main__':
    aoc.run()
