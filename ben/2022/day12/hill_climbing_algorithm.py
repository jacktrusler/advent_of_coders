import aoc
from collections import deque
import numpy as np
from numpy.typing import NDArray


Point = tuple[int, int]
HIGHEST = ord('z') - ord('a') + 2
ELEVATION_A = 1
LOWEST = 0

def adjacent_points(shape: tuple[int,int], point: Point) -> set[Point]:
    adj = [
        (point[0] + 1, point[1]), (point[0] - 1, point[1]),
        (point[0], point[1] + 1), (point[0], point[1] - 1)
    ]
    return {p for p in adj if (0 <= p[0] < shape[0]) and (0 <= p[1] < shape[1])}

def bfs(grid: NDArray, start: Point, end_value: int):
    start_value = grid[start]
    increasing = start_value < end_value
    
    queue = deque([(0, start)])
    visited = set()

    while queue:
        distance, point = queue.popleft()

        point_val = grid[point]
        if grid[point] == end_value:
            return distance
        if point in visited:
            continue
        visited.add(point)

        for adj in adjacent_points(grid.shape, point) - visited:
            adj_val = grid[adj]
            diff = (adj_val - point_val) * (1 if increasing else -1)
            if diff > 1:
                continue
            queue.append((distance + 1, adj))

def convert_letter(char: str) -> int:
    match char:
        case 'S': return LOWEST
        case 'E': return HIGHEST
        case _: return ord(char) - ord('a') + ELEVATION_A


@aoc.register(__file__)
def answers():
    height_map = np.vectorize(convert_letter)(aoc.read_grid())

    start = list(zip(*np.where(height_map == LOWEST)))[0]
    yield bfs(height_map, start, HIGHEST)

    height_map[height_map == LOWEST] = ELEVATION_A
    start = list(zip(*np.where(height_map == HIGHEST)))[0]
    yield bfs(height_map, start, ELEVATION_A)

if __name__ == '__main__':
    aoc.run()
