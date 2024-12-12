from itertools import pairwise

def explore_region(grid: dict, x: int, y: int, explored: set = None) -> set:
    if explored is None:
        explored = set()
    explored.add((x, y))
    for x2, y2 in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if (x2, y2) not in explored and grid[x, y] == grid.get((x2, y2), None):
            explored.update(explore_region(grid, x2, y2, explored))
    return explored

def count_sides(*perimeter_lists) -> int:
    num_sides = 0
    for p in perimeter_lists:
        num_sides += 1
        for (x1, y1), (x2, y2) in pairwise(sorted(p)):
            if x1 != x2 or y2 - y1 != 1:
                num_sides += 1
    return num_sides

def solve(puzzle_input: str) -> tuple[int]:
    garden = dict()
    for i, row in enumerate(puzzle_input.splitlines()):
        for j, v in enumerate(row):
            garden[i, j] = v
    searched = set()
    price_a = 0
    price_b = 0
    for (x, y), plant in garden.items():
        if (x, y) in searched:
            continue
        region = explore_region(garden, x, y)
        searched.update(region)
        top, bottom, left, right = list(), list(), list(), list()
        for rx, ry in region:
            if garden.get((rx-1, ry), None) != plant:
                top.append((rx, ry))
            if garden.get((rx+1, ry), None) != plant:
                bottom.append((rx, ry))
            if garden.get((rx, ry-1), None) != plant:
                left.append((ry, rx))
            if garden.get((rx, ry+1), None) != plant:
                right.append((ry, rx))
        price_a += len(region) * sum(len(side) for side in (top, bottom, left, right))
        price_b += len(region) * count_sides(top, bottom, left, right)
    return price_a, price_b

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "12.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
