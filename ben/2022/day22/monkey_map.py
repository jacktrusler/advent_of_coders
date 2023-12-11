from __future__ import annotations
import aoc
from dataclasses import dataclass
import itertools
import numpy as np
from numpy.typing import NDArray
import re


class CollisionError(Exception):
    pass

class MonkeyMap:
    @dataclass
    class State:
        point: aoc.Point
        direction: aoc.Direction
        shape: aoc.Point = None

        @property
        def password(self) -> int:
            DIRECTION_POINTS = {
                aoc.Direction.RIGHT: 0, aoc.Direction.DOWN: 1, aoc.Direction.LEFT: 2, aoc.Direction.UP: 3
            }
            return 4 * (self.point.x + 1) + 1000 * (self.point.y + 1) + DIRECTION_POINTS[self.direction]
        
        def move(self) -> MonkeyMap.State:
            return MonkeyMap.State(
                point = (self.point + self.direction.movement) % self.shape,
                direction = self.direction,
                shape = self.shape
            )
    
    def __init__(self, map_data: str):
        grid = self._grid(map_data)
        self.start = MonkeyMap.State(
            point = aoc.Point(np.where(grid[0] != ' ')[0][0], 0),
            direction = aoc.Direction.RIGHT,
            shape = aoc.Point(grid.shape[1], grid.shape[0])
        )
        self._open_tiles = set(aoc.np.points(grid == '.'))
        self._walls = set(aoc.np.points(grid == '#'))

    def _grid(self, map_data: str) -> NDArray:
        lines = map_data.splitlines()
        max_len = max(len(line) for line in lines)
        return np.array([list(x + ' ' * (max_len - len(x))) for x in map_data.splitlines()])

    def _move(self, state: MonkeyMap.State) -> MonkeyMap.State:
        new_state = state.move()
        if new_state.point in self._open_tiles: return new_state
        if new_state.point in self._walls: raise CollisionError
        return self._move(new_state)
    
    def navigate(self, cmds: list[str]) -> MonkeyMap.State:
        state = self.start
        for cmd in cmds:
            if cmd in ('R', 'L'):
                state.direction = state.direction.rotate(clockwise = cmd == 'R')
                continue

            for _ in range(int(cmd)):
                try:
                    state = self._move(state)
                except CollisionError:
                    break
        return state


class CubeMonkeyMap(MonkeyMap):
    @dataclass
    class State(MonkeyMap.State):
        face: CubeMonkeyMap.Face = None

        def move(self) -> CubeMonkeyMap.State:
            p = self.point + self.direction.movement
            if p in self.face:
                return CubeMonkeyMap.State(point=p, direction=self.direction, face=self.face)
            neighbor = self.face.neighbors[self.direction]
            entrance = self.face.entrance(neighbor)
            my_corner, neighbor_corner = self.face.corner(self.direction), neighbor.corner(entrance)
            dist = (self.point - my_corner).manhattan_distance()
            p = neighbor_corner + entrance.rotate(1).movement * (self.face.edge_size - dist - 1)
            return CubeMonkeyMap.State(point=p, direction=entrance.rotate(2), face=neighbor)

    class Face:
        def __init__(self, top_left: aoc.Point, edge_size: int):
            self.top_left = top_left
            self.edge_size = edge_size
            self.neighbors: dict[aoc.Direction, CubeMonkeyMap.Face] = {d: None for d in aoc.Direction}

        def __contains__(self, point: aoc.Point) -> bool:
            bottom_right = self.corner(aoc.Direction.DOWN)
            return self.top_left.x <= point.x <= bottom_right.x and self.top_left.y <= point.y <= bottom_right.y
        
        def __eq__(self, other: CubeMonkeyMap.Face) -> bool:
            if other is None: return False
            return self.top_left == other.top_left
        
        def corner(self, direction: aoc.Direction) -> aoc.Point:
            match direction:
                case aoc.Direction.UP: return self.top_left
                case aoc.Direction.RIGHT: return self.top_left + (self.edge_size-1, 0)
                case aoc.Direction.DOWN: return self.top_left + (self.edge_size-1, self.edge_size-1)
                case aoc.Direction.LEFT: return self.top_left + (0, self.edge_size-1)
        
        @property
        def valid(self) -> bool:
            return None not in self.neighbors.values()
        
        def entrance(self, neighbor: CubeMonkeyMap.Face) -> aoc.Direction:
            return next(d for d, x in neighbor.neighbors.items() if x == self)
        
        def orient(self):
            if self.valid:
                return
            for dir, neighbor in self.neighbors.items():
                if neighbor is None:
                    continue
                facing = self.entrance(neighbor)

                for rotation in (1, -1):
                    rotated = dir.rotate(rotation)
                    rel_rotated = facing.rotate(2).rotate(rotation)
                    if self.neighbors[rotated] is not None or neighbor.neighbors[rel_rotated] is None:
                        continue
                    new_neighbor = neighbor.neighbors[rel_rotated]
                    neighbor_facing = neighbor.entrance(new_neighbor)
                    
                    self.neighbors[rotated] = new_neighbor
                    new_neighbor.neighbors[neighbor_facing.rotate(-rotation)] = self


    def __init__(self, map_data: str):
        super().__init__(map_data)

        grid = self._grid(map_data)
        edge_size = min(sum(row != ' ') for row in grid)
        self.faces: list[CubeMonkeyMap.Face] = []
        
        # Find all faces
        for y in range(0, len(grid), edge_size):
            for x in range(0, len(grid[0]), edge_size):
                if grid[y][x] != ' ':
                    self.faces.append(CubeMonkeyMap.Face(top_left=aoc.Point(x, y), edge_size=edge_size))
        
        # Get neighboring faces without rotating
        for face in self.faces:
            neighbor_faces = {
                face.top_left + (0, -edge_size): aoc.Direction.UP,
                face.top_left + (0, +edge_size): aoc.Direction.DOWN,
                face.top_left + (-edge_size, 0): aoc.Direction.LEFT,
                face.top_left + (+edge_size, 0): aoc.Direction.RIGHT,
            }
            for f in self.faces:
                try:
                    facing = neighbor_faces[f.top_left]
                except KeyError:
                    continue

                face.neighbors[facing] = f
                f.neighbors[facing.rotate(2)] = face

        # Find neighboring faces by rotating until all neighbors have been found
        cycle = itertools.cycle(self.faces)
        while not all(x.valid for x in self.faces):
            next(cycle).orient()

        # Set the starting state
        self.start = CubeMonkeyMap.State(
            point = self.start.point,
            direction = self.start.direction,
            face = next(x for x in self.faces if self.start.point in x)
        )


@aoc.register(__file__)
def answers():
    map_data, cmds = aoc.read_chunks()
    cmds = re.split(r'(R|L)', cmds)
    
    monkey_map = MonkeyMap(map_data)
    yield monkey_map.navigate(cmds).password

    monkey_map = CubeMonkeyMap(map_data)
    yield monkey_map.navigate(cmds).password

if __name__ == '__main__':
    aoc.run()
