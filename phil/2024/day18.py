import heapq

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def path_length(grid_size: int, obstacles: set):
    grid = dict()
    for x in range(grid_size):
        for y in range(grid_size):
            grid[x, y] = 1 if (x, y) in obstacles else 0
    visited = set()
    unvisited = [(0, 0, 0)]
    while unvisited:
        s, x, y = heapq.heappop(unvisited)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if x == grid_size - 1 and y == grid_size - 1:
            return s
        for dx, dy in DIRECTIONS:
            x2 = x + dx
            y2 = y + dy
            try:
                visitable = grid[x2, y2] != 1
            except KeyError:
                visitable = False
            if visitable:
                heapq.heappush(unvisited, (s+1, x2, y2))
    return None

def solve(puzzle_input: str) -> tuple[int]:
    grid_size = 71
    obstacles = [tuple(int(x) for x in line.split(',')) for line in puzzle_input.splitlines()]
    a = path_length(grid_size, set(obstacles[:1024]))
    imin = 1024
    imax = len(obstacles) + 1
    results = dict()
    b = None
    while True:
        i = imin + (imax - imin) // 2
        pathlen = path_length(grid_size, set(obstacles[:i+1]))
        if pathlen:
            imin = i
        else:
            imax = i+1
            try:
                done = results[i-1] is not None
            except KeyError:
                pass
            else:
                if done:
                    b = ','.join([str(n) for n in obstacles[i]])
                    break
        results[i] = pathlen
    return a, b

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "18.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
