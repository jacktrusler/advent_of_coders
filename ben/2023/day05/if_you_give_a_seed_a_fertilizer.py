from __future__ import annotations
import aoc
from aoc.utils import pairwise, Interval
from dataclasses import dataclass
from functools import reduce
from typing import Iterable, Generator


@dataclass(frozen=True)
class MapRule:
    delta: int
    bounds: Interval

@dataclass(frozen=True)
class AlmanacMap:
    rules: list[MapRule]

    @classmethod
    def from_string(cls, map_str: str) -> AlmanacMap:
        def _per_rule(r: str) -> MapRule:
            params = tuple(map(int, r.split()))
            return MapRule(
                delta = params[0] - params[1],
                bounds = Interval(params[1], params[1] + params[2] - 1)
            )
        return cls(list(map(_per_rule, map_str.splitlines()[1:])))
    
    def convert(self, values: Iterable[Interval]) -> Generator[Interval]:
        def _convert(val: Interval) -> Generator[Interval]:
            try:
                rule = next(x for x in self.rules if val in x.bounds)
            except StopIteration:
                yield val
                return
            
            yield (rule.bounds & val) + rule.delta
            for i in val.difference(rule.bounds):
                yield from _convert(i)

        for v in values:
            yield from _convert(v)


@aoc.register(__file__)
def answers():
    data = aoc.read_chunks()
    seeds = list(map(int, data[0].split(':')[1].split()))
    maps = [AlmanacMap.from_string(x) for x in data[1:]]
    
    seeds1 = [Interval(seed, seed) for seed in seeds]
    locations1 = reduce(lambda x, y: y.convert(x), maps, seeds1)
    yield min([x.start for x in locations1])

    seeds2 = [Interval(start, start+_len-1) for start, _len in pairwise(seeds)]
    locations2 = reduce(lambda x, y: y.convert(x), maps, seeds2)
    yield min([x.start for x in locations2])

if __name__ == '__main__':
    aoc.run()
