from __future__ import annotations
import aoc
from collections import Counter
import re


class Universe:
    def __init__(self, input: str):
        line_length = input.index('\n') + 1
        galaxies = list(divmod(m.start(), line_length) for m in re.finditer(r'#', input))
        y_vals, x_vals = zip(*galaxies)

        self.x_vals = Counter(x_vals)
        self.y_vals = Counter(y_vals)

    def total_dist(self, expansion: int) -> int:
        factor = expansion - 1
        def _expand(vals: Counter[int]):
            tot_amt = 0
            prev_i = 0
            remaining = sum(vals.values())
            for i, amt in sorted(vals.items()):
                traveled = i - prev_i
                empty_before = max(traveled - 1, 0)
                dist = traveled + (empty_before * factor)
                remaining -= amt
                movement = tot_amt * dist
                yield (amt * movement) + (remaining * movement)
                tot_amt += amt
                prev_i = i

        return sum((*_expand(self.x_vals), *_expand(self.y_vals)))


@aoc.register(__file__)
def answers():
    universe = Universe(aoc.read_data())
    yield universe.total_dist(expansion=2)
    yield universe.total_dist(expansion=1000000)

if __name__ == '__main__':
    aoc.run()
