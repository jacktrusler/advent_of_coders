import aoc
from aoc.utils import Interval


def parse_line(line: str) -> tuple[Interval, Interval]:
    a, b = line.split(',')
    ia = Interval(*map(int, a.split('-')))
    ib = Interval(*map(int, b.split('-')))
    return ia, ib

@aoc.register(__file__)
def answers():
    assignments = [parse_line(x) for x in aoc.read_lines()]
    yield sum([x < y or x > y for x, y in assignments])
    yield sum([x in y for x, y in assignments])

if __name__ == '__main__':
    aoc.run()
