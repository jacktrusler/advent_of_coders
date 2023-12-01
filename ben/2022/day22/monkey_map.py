from __future__ import annotations
import aoc
from dataclasses import dataclass
from enum import Enum
import numpy as np
from numpy.typing import NDArray
import re


Point = tuple[int, int]

class CollisionError(Exception):
    pass

class Facing(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def __add__(self, v: int):
        return Facing((self.value + v) % 4)

    def __sub__(self, v: int):
        return Facing((self.value - v) % 4)

class MonkeyMap:
    def __init__(self, map_data: str):
        lines = map_data.splitlines()
        max_len = max(len(line) for line in lines)
        self._grid = np.array([list(x + ' ' * (max_len - len(x))) for x in lines])
        self.start: Point = 0, np.where(self._grid[0] != ' ')[0][0]

    def move(self, p: Point, f: Facing) -> Point:
        vert_mod = 1 if f == Facing.DOWN else (-1 if f == Facing.UP else 0)
        horz_mod = 1 if f == Facing.RIGHT else (-1 if f == Facing.LEFT else 0)
        p = (p[0] + vert_mod) % self._grid.shape[0], (p[1] + horz_mod) % self._grid.shape[1]

        match self._grid[p]:
            case '.': return p
            case ' ': return self.move(p, f)
            case '#': raise CollisionError


class CubeMonkeyMap(MonkeyMap):
    class Face:
        def __init__(self, grid: NDArray, top_left: Point):
            self.top_left = top_left
            self._grid = grid
            self.neighbors: dict[Facing, tuple[CubeMonkeyMap.Face, Facing]] = {}
            self.size = len(self._grid)

        def __contains__(self, point: Point):
            return (self.top_left[0] <= point[0] < self.top_left[0] + self.size) and (self.top_left[1] <= point[1] < self.top_left[1] + self.size)

        def add_neighbor(self, neighbor: CubeMonkeyMap.Face, facing: Facing, entry: Facing):
            print(f'Add neighbor: {facing}, {entry}')
            self.neighbors[facing] = (neighbor, entry)
            neighbor.neighbors[entry] = (self, facing)

            shared_neighbors = (Facing.UP, Facing.DOWN) if facing in (Facing.LEFT, Facing.RIGHT) else (Facing.LEFT, Facing.RIGHT)
            print(f'Shared neighbors: {shared_neighbors}')
            for f in shared_neighbors:
                if f not in self.neighbors:
                    continue
                shared_neighbor, sn_entry = self.neighbors[f]
                _f = f - (facing + 2 - entry.value).value
                _e = f + (entry - sn_entry.value).value
                if _e in shared_neighbor.neighbors:
                    continue
                print(f'auto add neighbor: {_f}, {_e}')
                neighbor.add_neighbor(shared_neighbor, facing=_f, entry=_e)

        def find_neighbors(self, grid: NDArray):
            print(f'find neighbors for:\n{self._grid}')
            dirs = {
                Facing.RIGHT: (self.top_left[0], self.top_left[1] + self.size),
                Facing.DOWN: (self.top_left[0] + self.size, self.top_left[1]),
                Facing.LEFT: (self.top_left[0], self.top_left[1] - self.size),
                Facing.UP: (self.top_left[0] - self.size, self.top_left[1])
            }

            for f, p in dirs.items():
                if ((p[0] < 0 or p[0] >= grid.shape[0] or p[1] < 0 or p[1] >= grid.shape[1]) or grid[p] == ' ' or f in self.neighbors):
                    continue
                print(f'Neighbor found at {p}. Direction {f}')
                new_face = grid[p[0]:p[0] + self.size, p[1]:p[1] + self.size]
                new_face = CubeMonkeyMap.Face(new_face, p)
                print(f'Neighbor grid:\n{new_face._grid}')
                self.add_neighbor(new_face, facing=f, entry=f+2)
                new_face.find_neighbors(grid)




    def __init__(self, map_data: str, cube_size: int):
        lines = map_data.splitlines()
        max_len = max(len(line) for line in lines)
        grid = np.array([list(x + ' ' * (max_len - len(x))) for x in lines])

        self.start: Point = 0, np.where(grid[0] != ' ')[0][0]
        front_face = grid[self.start[0]:self.start[0] + cube_size, self.start[1]:self.start[1] + cube_size]
        front_face = CubeMonkeyMap.Face(front_face, self.start)
        front_face.find_neighbors(grid)
                

    def move(self, p: Point, f: Facing) -> Point:
        pass


def navigate(monkey_map: MonkeyMap, cmds: list[str], facing: Facing) -> tuple[Point, Facing]:
    point = monkey_map.start
    for cmd in cmds:
        try:
            movements = int(cmd)
        except ValueError:
            facing += 1 if cmd == 'R' else -1
            continue
        
        for _ in range(movements):
            try:
                point = monkey_map.move(point, facing)
            except CollisionError:
                break
    return point, facing

def password(point: Point, facing: Facing) -> int:
    return 1000 * (point[0] + 1) + 4 * (point[1] + 1) + facing.value


@aoc.register(__file__)
def answers():
    data = 'small'
    map_data, cmds = aoc.read_chunks(data)
    cmds = re.split(r'(R|L)', cmds)
    
    monkey_map = MonkeyMap(map_data)
    point, facing = navigate(monkey_map, cmds, Facing.RIGHT)
    yield password(point, facing)

    cube_size = 50 if data != 'small' else 4
    monkey_map = CubeMonkeyMap(map_data, cube_size=cube_size)
    point, facing = navigate(monkey_map, cmds, Facing.RIGHT)
    yield password(point, facing)

if __name__ == '__main__':
    aoc.run()
