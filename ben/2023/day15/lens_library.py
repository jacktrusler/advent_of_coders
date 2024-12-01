import aoc
from collections import defaultdict, OrderedDict
import functools


def HASH(step: str) -> int:
    _per_char = lambda x, c: (((x + ord(c)) * 17) % 256)
    return functools.reduce(lambda x, c: _per_char(x, c), step, 0)

def HASH_MAP(steps: list[str]) -> dict:
    def _per_step(_map: dict, step: str):
        if step[-1] == '-':
            label = step[:-1]
            _map[HASH(label)].pop(label, None)
        else:
            label, focus = step.split('=')
            _map[HASH(label)][label] = int(focus)
        return _map
    return functools.reduce(lambda m, step: _per_step(m, step), steps, defaultdict(OrderedDict))

def focusing_power(hash_map: dict) -> int:
    _per_box = lambda id, x: sum((id+1) * i * focus for i, focus in enumerate(x.values(), start=1))
    return sum(_per_box(box, lenses) for box, lenses in hash_map.items())


@aoc.register(__file__)
def answers():
    steps = aoc.read_data().split(',')
    yield sum(map(HASH, steps))
    yield focusing_power(HASH_MAP(steps))

if __name__ == '__main__':
    aoc.run()
