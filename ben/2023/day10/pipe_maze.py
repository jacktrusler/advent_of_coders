from __future__ import annotations
import aoc
from aoc.utils import adjacent_points
import numpy as np
from numpy.typing import NDArray


Loop = list[aoc.Point]

CONNECTABLE = {
    aoc.Direction.UP: 'S|7F',
    aoc.Direction.RIGHT: 'S-J7',
    aoc.Direction.DOWN: 'S|LJ',
    aoc.Direction.LEFT: 'S-LF',
}

def travel(pipe: str, dir: aoc.Direction) -> aoc.Direction:
    match pipe:
        case '|'|'-': return dir
        case 'L': return aoc.Direction.RIGHT if dir == aoc.Direction.DOWN else aoc.Direction.UP
        case 'J': return aoc.Direction.LEFT if dir == aoc.Direction.DOWN else aoc.Direction.UP
        case '7': return aoc.Direction.LEFT if dir == aoc.Direction.UP else aoc.Direction.DOWN
        case 'F': return aoc.Direction.RIGHT if dir == aoc.Direction.UP else aoc.Direction.DOWN

def find_loop(grid: NDArray, start: aoc.Point) -> Loop:
    def _try_find_loop(dir: aoc.Direction):
        visited = [start]
        point = start + dir.movement
        while point != start:
            visited.append(point)
            if (pipe := grid[point.y][point.x]) not in CONNECTABLE[dir]:
                return None
            dir = travel(pipe, dir)
            point = point + dir.movement
        return visited

    for dir in aoc.Direction:
        if (loop := _try_find_loop(dir)) is not None:
            return loop

def replace_S(start: aoc.Point, first: aoc.Point, last: aoc.Point) -> str:
    dirs = {dir for dir, adj in adjacent_points(start, include_dir=True) if adj == first or adj == last}
    new_value = set.intersection(*(set(CONNECTABLE[x.rotate(2)]) for x in dirs)) - {'S'}
    return next(iter(new_value))

def enclosed_tiles(grid: NDArray, loop: Loop) -> set[aoc.Point]:
    pts = aoc.np.indexes(loop)
    _grid = np.full_like(grid, fill_value='.')
    _grid[pts] = grid[pts]

    rolled = np.roll(_grid, -1, axis=1)
    while np.isin(_grid, ['F', 'L']).any():
        f, l = _grid == 'F', _grid == 'L'
        seven, j = rolled == '7', rolled == 'J'

        _grid = np.select(
            [np.logical_or(f & j, l & seven), np.logical_or(f & seven, l & j)],
            ['|', '.'],
            _grid
        )
        rolled = np.roll(rolled, -1, axis=1)
    
    count = np.cumsum(_grid == '|', axis=1)
    count[pts] = 0
    return set(aoc.np.points(count % 2 == 1))


@aoc.register(__file__)
def answers():
    grid = np.array(aoc.read_grid())
    start = next(aoc.np.points(grid == 'S'))

    loop = find_loop(grid, start)
    yield len(loop) // 2

    first, last = loop[1], loop[-1]
    grid[start.y][last.x] = replace_S(start, first, last)
    yield len(enclosed_tiles(grid, loop))

if __name__ == '__main__':
    aoc.run()
