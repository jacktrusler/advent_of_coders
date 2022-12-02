import aoc
from math import prod
import numpy as np
from numpy.typing import NDArray


def find_low_points(height_map: NDArray) -> NDArray:
    padded_map = np.pad(height_map, 1, constant_values=10)
    left = height_map < padded_map[1:-1, :-2]
    right = height_map < padded_map[1:-1, 2:]
    up = height_map < padded_map[:-2, 1:-1]
    down = height_map < padded_map[2:, 1:-1]
    low = left & right & up & down
    return np.where(low == True)

def find_basin(height_map: NDArray, point:tuple, indices=None):
    def _basin_points(point: tuple, points: set[tuple] = set()) -> set[tuple]:
        try:
            if height_map[point] == 9 or -1 in point or point in points:
                return set()
        except IndexError:
            return set()
        points.add(point)
        points |= _basin_points((point[0]+1, point[1]), points)
        points |= _basin_points((point[0]-1, point[1]), points)
        points |= _basin_points((point[0], point[1]+1), points)
        points |= _basin_points((point[0], point[1]-1), points)
        return points

    return _basin_points(point)


@aoc.register(__file__)
def answers():
    height_map = np.array(aoc.read_grid(), dtype=int)
    
    low_points = find_low_points(height_map)
    yield sum(height_map[low_points] + 1)

    basins = [find_basin(height_map, x) for x in zip(low_points[0], low_points[1])]
    sizes = sorted(list(map(len, basins)))
    yield prod(sizes[-3:])

if __name__ == '__main__':
    aoc.run()
