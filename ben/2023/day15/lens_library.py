import aoc
from collections import defaultdict, OrderedDict
import functools
import re


def HASH(step: str) -> int:
    per_char = lambda x, c: (((x + ord(c)) * 17) % 256)
    return functools.reduce(lambda x, c: per_char(x, c), step, 0)

def HASH_MAP(steps: list[str]) -> int:
    def _per_step(_map: dict, step: str):
        m = re.match(r'(?P<label>.*)(?P<op>=|-)(?P<focus>\d+)?', step).groupdict()
        box = HASH(m['label'])
        match m['op']:
            case '=': _map[box][m['label']] = int(m['focus'])
            case '-': _map[box].pop(m['label'], None)
        return _map
    hash_map = functools.reduce(lambda m, step: _per_step(m, step), steps, defaultdict(OrderedDict))

    per_box = lambda box, lenses: sum((box+1) * i * focus for i, focus in enumerate(lenses.values(), start=1))
    return sum(per_box(box, lenses) for box, lenses in hash_map.items())


@aoc.register(__file__)
def answers():
    steps = aoc.read_data().split(',')
    yield sum(map(HASH, steps))
    yield HASH_MAP(steps)

if __name__ == '__main__':
    aoc.run()
