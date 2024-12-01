from __future__ import annotations
import aoc
from typing import Iterable


Instruction = tuple[aoc.Direction, int]
def parse_line(line: str) -> tuple[Instruction, Instruction]:
    dir, n, color = line.split()
    match dir:
        case 'U': dir = aoc.Direction.UP
        case 'R': dir = aoc.Direction.RIGHT
        case 'D': dir = aoc.Direction.DOWN
        case 'L': dir = aoc.Direction.LEFT
    color = color[2:-1]
    match color[-1]:
        case '0': dir2 = aoc.Direction.RIGHT
        case '1': dir2 = aoc.Direction.DOWN
        case '2': dir2 = aoc.Direction.LEFT
        case '3': dir2 = aoc.Direction.UP
    n2 = int(color[:5], 16)
    return (dir, int(n)), (dir2, n2)

def trench_area(dig_plan: Iterable[Instruction], start: aoc.Point = aoc.Point(0, 0)) -> int:
    loc = start
    perimeter = 0
    vertices: list[aoc.Point] = []
    for instruction in dig_plan:
        perimeter += instruction[1]
        loc = loc.move(instruction[0], instruction[1])
        vertices.append(loc)

    # Combination of shoelace theorem and Pick's theorem
    next_verts = vertices[1:] + [vertices[0]]
    area = sum((a[0] * b[1] - a[1] * b[0]) for a, b in zip(vertices, next_verts))
    return (area // 2) + (perimeter // 2) + 1


@aoc.register(__file__)
def answers():
    dig_plan1, dig_plan2 = zip(*map(parse_line, aoc.read_lines()))
    yield trench_area(dig_plan1)
    yield trench_area(dig_plan2)

if __name__ == '__main__':
    aoc.run()
