from __future__ import annotations
import aoc
from aoc.utils import pairwise
from dataclasses import dataclass
from functools import reduce
from typing import Iterable, Generator


@dataclass
class Range:
    start: int
    end: int

@dataclass
class MapRule:
    dest_start: int
    src_start: int
    src_end: int

    def __contains__(self, val: int | Range) -> bool:
        match val:
            case int(): return self.src_start <= val < self.src_end
            case Range(): return val.end > self.src_start and val.start < self.src_end
            
    def apply(self, val: int | Range) -> int:
        match val:
            case int(): return (val - self.src_start) + self.dest_start
            case Range(): return Range(
                start = self.apply(max(val.start, self.src_start)),
                end = self.apply(min(val.end, self.src_end)),
            )

class AlmanacMap:
    def __init__(self, rules: list[MapRule]):
        self.rules = rules

    def convert(self, val: int | Range) -> Generator[int | Range]:
        for rule in self.rules:
            if val in rule:
                yield rule.apply(val)
                if type(val) is Range:
                    if val.end-1 not in rule:
                        yield from self.convert(Range(rule.src_end, val.end))
                    if val.start not in rule:
                        yield from self.convert(Range(val.start, rule.src_start))
                return
        yield val
    
    def convert_all(self, values: Iterable[int | Range]) -> Generator[int | Range]:
        for v in values:
            yield from self.convert(v)

    @staticmethod
    def from_string(map_str: str) -> AlmanacMap:
        rules = []
        for rule in map_str.splitlines()[1:]:
            params = tuple(map(int, rule.split()))
            rules.append(MapRule(
                dest_start = params[0],
                src_start = params[1],
                src_end = params[1] + params[2]
            ))
        return AlmanacMap(rules)


@aoc.register(__file__)
def answers():
    data = aoc.read_chunks('small')
    seeds = list(map(int, data[0].split(':')[1].split()))
    maps = [AlmanacMap.from_string(x) for x in data[1:]]
    
    part_one = reduce(lambda x, y: y.convert_all(x), maps, seeds)
    yield min(part_one)

    part_two = [Range(start=start, end=start+_len) for start, _len in pairwise(seeds)]
    part_two = reduce(lambda x, y: y.convert_all(x), maps, part_two)
    yield min([x.start for x in part_two])

if __name__ == '__main__':
    aoc.run()
