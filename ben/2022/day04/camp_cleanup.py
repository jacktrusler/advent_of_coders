import aoc
import re


def parse_line(line: str) -> tuple[set,set]:
    m = tuple(map(int, re.match(r'(\d+)-(\d+),(\d+)-(\d+)', line).groups()))
    return set(range(m[0], m[1]+1)), set(range(m[2], m[3]+1))


@aoc.register(__file__)
def answers():
    assignments = [parse_line(x) for x in aoc.read_lines()]
    yield len([x for x in assignments if x[0] <= x[1] or x[1] <= x[0]])
    yield len([x for x in assignments if x[0] & x[1]])

if __name__ == '__main__':
    aoc.run()
