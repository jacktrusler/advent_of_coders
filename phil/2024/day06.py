DIRECTIONS = {(-1, 0): (0, 1), (0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0)}

def patrol(size: int, obstacles: set, x: int, y: int, dx: int, dy: int):
    while True:
        x2 = x + dx
        y2 = y + dy
        if (x2, y2) in obstacles:
            dx, dy = DIRECTIONS[dx, dy]
        else:
            x = x2
            y = y2
            if 0 <= x < size and 0 <= y < size:
                yield x, y, dx, dy
            else:
                break

def position_from_index(grid_size, i):
    return i // (grid_size + 1), i % (grid_size + 1)

def solve(puzzle_input: str):
    grid_size = puzzle_input.index('\n')
    obstacles = {position_from_index(grid_size, i) for i, v in enumerate(puzzle_input) if v == '#'}
    x, y = position_from_index(grid_size, puzzle_input.index('^'))
    dx, dy = list(DIRECTIONS.keys())[0]
    visited = set(((x, y),))
    visited_dir = set(((x, y, dx, dy),))
    loop_obstacles = set()
    for x2, y2, dx2, dy2 in patrol(grid_size, obstacles, x, y, dx, dy):
        if (x2, y2) not in obstacles and (x2, y2) not in visited:
            visited_dir_2 = set()
            for x3, y3, dx3, dy3 in patrol(grid_size, obstacles | {(x2, y2)}, x, y, dx, dy):
                if (x3, y3, dx3, dy3) in visited_dir or (x3, y3, dx3, dy3) in visited_dir_2:
                    loop_obstacles.add((x2, y2))
                    break
                visited_dir_2.add((x3, y3, dx3, dy3))
        x, y, dx, dy = x2, y2, dx2, dy2
        visited.add((x, y))
        visited_dir.add((x, y, dx, dy))
    return len(visited), len(loop_obstacles)

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "06.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
