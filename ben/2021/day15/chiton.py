from __future__ import annotations
import aoc
import heapq
import numpy as np
from numpy.typing import NDArray


def adjacent_points(shape: tuple[int,int], point: tuple[int,int]) -> set[tuple[int,int]]:
    adj = [
        (point[0] + 1, point[1]), (point[0] - 1, point[1]),
        (point[0], point[1] + 1), (point[0], point[1] - 1)
    ]
    return {p for p in adj if (0 <= p[0] < shape[0]) and (0 <= p[1] < shape[1])}

def manhattan_dist(point1: tuple[int,int], point2: tuple[int,int]) -> int:
    return abs(point2[0] - point1[0]) + abs(point2[1] - point2[1])

def astar(grid: NDArray) -> int:
    start = (0, 0)
    end = (grid.shape[0] - 1, grid.shape[1] - 1)
    
    path_stack = []
    visited = set()
    heapq.heappush(path_stack, (0, 0, start))

    while path_stack:
        _, true_value, point = heapq.heappop(path_stack)
        if point == end:
            return true_value
        if point in visited:
            continue
        visited.add(point)

        adjacents = adjacent_points(grid.shape, point) - visited
        for adj in adjacents:
            true = true_value + grid[adj[1]][adj[0]]
            f = manhattan_dist(adj, end) + true
            heapq.heappush(path_stack, (f, true, adj))

def expand_grid(grid: NDArray, n: int) -> NDArray:
    vertical = np.vstack([grid + row for row in range(n)])
    full_grid = np.hstack([vertical + col for col in range(n)])
    return np.where(full_grid > 9, full_grid - 9, full_grid)
    

@aoc.register(__file__)
def answers():
    grid = np.array(aoc.read_grid(), dtype=int)
    yield astar(grid)

    grid = expand_grid(grid, 5)
    yield astar(grid)

if __name__ == '__main__':
    aoc.run(profile=True)
