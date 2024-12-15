from statistics import variance
from math import prod

WIDTH = 101
HEIGHT = 103

def display(robots: list[tuple[int, int]]) -> None:
    robot_grid = ['.'] * range(WIDTH) * range(HEIGHT)
    for (x, y) in robots:
        robot_grid[y][x] = '#'
    for row in robot_grid:
        print(''.join(row))

def safety_factor(x: list[int], y: list[int]) -> int:
    quadrants = [0, 0, 0, 0]
    xsplit = (WIDTH - 1) / 2
    ysplit = (HEIGHT - 1) / 2
    for x2, y2 in zip(x, y):
        if x2 < xsplit and y2 < ysplit:
            quadrants[0] += 1
        elif x2 < xsplit and y2 > ysplit:
            quadrants[1] += 1
        elif x2 > xsplit and y2 < ysplit:
            quadrants[2] += 1
        elif  x2 > xsplit and y2 > ysplit:
            quadrants[3] += 1
    return prod(quadrants)

def position(robots: list[tuple[int, int]], bound: int, num_seconds: int) -> list[int]:
    return [(pos + (vel * num_seconds)) % bound for pos, vel in robots]

def solve(puzzle_input: str) -> tuple[int]:
    x, y = list(), list()
    for line in puzzle_input.splitlines():
        ptext, vtext = line.split(" ")
        px, py = (int(x) for x in ptext[2:].split(','))
        vx, vy = (int(x) for x in vtext[2:].split(','))
        x.append((px, vx))
        y.append((py, vy))

    safety = safety_factor(position(x, WIDTH, 100), position(y, HEIGHT, 100))
    
    var_x = (variance(position(x, WIDTH, i)) for i in range(WIDTH))
    start_x = min(enumerate(var_x), key=lambda n: n[1])[0]
    x_cycles = set(range(start_x, WIDTH * HEIGHT, WIDTH))

    var_y = (variance(position(y, HEIGHT, i)) for i in range(HEIGHT))
    start_y = min(enumerate(var_y), key=lambda n: n[1])[0]
    y_cycles = set(range(start_y, WIDTH * HEIGHT, HEIGHT))

    min_index = min(x_cycles & y_cycles)
    return safety, min_index

if __name__ == '__main__':
    from pathlib import Path
    import aoc_util
    input_path = Path(__file__).parent / "input" / "14.txt"
    aoc_util.report(*aoc_util.run_solution(solve, input_path))
