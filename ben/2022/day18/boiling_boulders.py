import aoc
from collections import deque
import itertools
import numpy as np


def directions():
    yield from ((1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1))

Point = tuple[int, int, int]
def bounding_box(cubes: set[Point], point: Point, ranges: tuple[range], seen: set[Point]) -> tuple[set[Point], int]:
    queue = deque([point])
    visited = set()
    faces = 0

    while queue:
        pt = queue.pop()
        if pt in visited:
            continue
        if pt in seen:
            return visited, 0

        visited.add(pt)
        if any(axis not in r for axis, r in zip(pt, ranges)):
            return visited, 0

        for dir in directions():
            adj = pt[0] + dir[0], pt[1] + dir[1], pt[2] + dir[2]
            if adj in visited:
                continue

            if adj in cubes:
                faces += 1
            else:
                queue.append(adj)
    return visited, faces


@aoc.register(__file__)
def answers():
    cubes = np.array([tuple(map(int, line.split(','))) for line in aoc.read_lines()])
    cube_set = set(zip(*cubes.T))
    adj = [set(zip(*(cubes + dir).T)) for dir in directions()]

    matching_sides = sum(len(cube_set & x) for x in adj)
    surface_area = 6 * len(cubes) - matching_sides
    yield surface_area

    ranges = (
        range(min(cubes[:,0]), max(cubes[:,0]) + 1),
        range(min(cubes[:,1]), max(cubes[:,1]) + 1),
        range(min(cubes[:,2]), max(cubes[:,2]) + 1)
    )
    seen = set()
    for p in itertools.product(*ranges):
        if p in cube_set:
            continue
        visited, faces = bounding_box(cube_set, p, ranges, seen)
        surface_area -= faces
        seen |= visited
    yield surface_area
    
if __name__ == '__main__':
    aoc.run()
