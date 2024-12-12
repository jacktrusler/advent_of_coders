import aoc
from aoc.utils import quadratic
import math


def win_possibilities(max_time: int, distance: int) -> int:
    min_t, max_t = quadratic(-1, max_time, -distance)
    return math.floor(max_t) - math.ceil(min_t) + 1


@aoc.register(__file__)
def answers():
    data = [x.split(':')[1] for x in aoc.read_lines()]

    times, distances = [list(map(int, x.split())) for x in data]
    yield math.prod(map(win_possibilities, times, distances))

    time, distance = [int(x.replace(' ', '')) for x in data]
    yield win_possibilities(time, distance)

if __name__ == '__main__':
    aoc.run()
