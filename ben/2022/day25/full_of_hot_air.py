import aoc
import math
from typing import Generator


FROM_MAP = {'=': -2, '-': -1, '0': 0, '1': 1, '2': 2}
def from_snafu(val: str) -> int:
    return sum(5**i * FROM_MAP[v] for i, v in enumerate(reversed(val)))


def vals(i, v) -> Generator[str, int]:
    p = 5**i
    yield from {
        '2': v - 2*p,
        '1': v - p,
        '0': v,
        '-': v + p,
        '=': v + 2*p,
    }.items()

def to_snafu(val: int) -> str:
    num_digits = math.ceil(math.log(val/2, 5)) + 1
    retval = ''

    for i in reversed(range(num_digits)):
        action, val = min(vals(i, val), key=lambda x: abs(x[1]))
        retval += action
    return retval


@aoc.register(__file__)
def answers():
    values = [from_snafu(x) for x in aoc.read_lines()]
    yield to_snafu(sum(values))

if __name__ == '__main__':
    aoc.run()
