import aoc
from functools import reduce
import math


def quadratic(a: int, b: int, c: int) -> tuple[float, float]:
    _sqrt = math.sqrt(b**2 - 4*a*c)
    _denom = 2*a
    return sorted(((-b + _sqrt) / _denom, (-b - _sqrt) / _denom))

def win_possibilities(max_time: int, distance: int) -> int:
    min_t, max_t = quadratic(-1, max_time, -distance)
    return math.ceil(max_t-1) - math.floor(min_t+1) + 1


@aoc.register(__file__)
def answers():
    data = [x.split(':')[1] for x in aoc.read_lines()]

    times, distances = [list(map(int, x.split())) for x in data]
    part_one = [win_possibilities(t, d) for t, d in zip(times, distances)]
    yield reduce(lambda x, y: x * y, part_one)

    time, distance = [int(x.replace(' ', '')) for x in data]
    yield win_possibilities(time, distance)


if __name__ == '__main__':
    aoc.run()
