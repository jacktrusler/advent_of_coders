from __future__ import annotations
import aoc
from aoc.utils import pairwise, Interval
from dataclasses import dataclass
from functools import reduce
from typing import Iterable, Generator


@dataclass
class MapRule:
    delta: int
    bounds: Interval

class AlmanacMap:
    def __init__(self, rules: list[MapRule]):
        self.rules = rules

    def convert(self, val: Interval) -> Generator[Interval]:
        for rule in self.rules:
            if val in rule.bounds:
                yield (rule.bounds & val) + rule.delta

                for i in val.difference(rule.bounds):
                    yield from self.convert(i)
                return
        yield val
    
    def convert_all(self, values: Iterable[Interval]) -> Generator[Interval]:
        for v in values:
            yield from self.convert(v)

    @staticmethod
    def from_string(map_str: str) -> AlmanacMap:
        rules = []
        for rule in map_str.splitlines()[1:]:
            params = tuple(map(int, rule.split()))
            rules.append(MapRule(
                delta = params[0] - params[1],
                bounds = Interval(start = params[1], end = params[1] + params[2] - 1)
            ))
        return AlmanacMap(rules)


@aoc.register(__file__)
def answers():
    data = aoc.read_chunks()
    seeds = list(map(int, data[0].split(':')[1].split()))
    maps = [AlmanacMap.from_string(x) for x in data[1:]]
    
    seeds1 = [Interval(start=seed, end=seed) for seed in seeds]
    locations1 = reduce(lambda x, y: y.convert_all(x), maps, seeds1)
    yield min([x.start for x in locations1])

    seeds2 = [Interval(start=start, end=start+_len-1) for start, _len in pairwise(seeds)]
    locations2 = reduce(lambda x, y: y.convert_all(x), maps, seeds2)
    yield min([x.start for x in locations2])

if __name__ == '__main__':
    aoc.run()
