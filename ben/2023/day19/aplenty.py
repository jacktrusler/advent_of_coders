from __future__ import annotations
import aoc
from aoc.utils import Interval
from collections import deque
from dataclasses import dataclass, field, replace
from operator import lt, gt
from math import prod
import re
from typing import Iterable, Callable, Generator


@dataclass(frozen=True)
class MachinePart:
    x: Interval
    m: Interval
    a: Interval
    s: Interval

    def __getitem__(self, key: str) -> Interval:
        return getattr(self, key)
    
    @classmethod
    def from_string(cls, ratings: str) -> MachinePart:
        m = re.match(r'{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}', ratings).groupdict()
        return cls(**{k: Interval(int(v), int(v)) for k, v in m.items()})

    @property
    def rating(self) -> int:
        return sum(v.start for v in (self.x, self.m, self.a, self.s))
    
    @property
    def possibilities(self) -> int:
        return prod(len(v) for v in (self.x, self.m, self.a, self.s))
    
    def replace(self, key: str, val: Interval) -> MachinePart:
        return replace(self, **{key: val})


@dataclass(frozen=True)
class Workflow:
    id: str
    rules: list[Workflow.Rule] = field(default_factory=list)

    @dataclass(frozen=True)
    class Rule:
        destination: str
        category: str = None
        operation: Callable[[int, int], bool] = None
        value: int = None

        @classmethod
        def from_string(cls, rule: str) -> Workflow.Rule:
            if ':' not in rule:
                return cls(rule)
            m = re.match(r'(?P<category>.*)(?P<cond>[<>])(?P<value>\d+):(?P<destination>.*)', rule).groupdict()
            op = lt if m['cond'] == '<' else gt
            return cls(m['destination'], m['category'], op, int(m['value']))

        def allow(self, part: MachinePart) -> bool:
            return self.operation(part[self.category].start, self.value) if self.category else True
        
        def filter(self, part: MachinePart) -> tuple[MachinePart, MachinePart]:
            if self.category is None:
                return part, None
            if not (v := part[self.category]) & self.value:
                return None, part
            
            below = Interval(v.start, self.value-1 if self.operation == lt else self.value)
            above = Interval(self.value+1 if self.operation == gt else self.value, v.end)
            passed = below if self.operation == lt else above
            failed = above if self.operation == lt else below
            return part.replace(self.category, passed), part.replace(self.category, failed)

    @classmethod
    def from_string(cls, workflow: str) -> Workflow:
        id, rules = re.match(r'(?P<id>.*){(?P<rules>.*)}', workflow).groups()
        rules = list(map(Workflow.Rule.from_string, rules.split(',')))
        return cls(id, rules)

    def process(self, part: MachinePart) -> str:
        for rule in self.rules:
            if rule.allow(part):
                return rule.destination

    def filter(self, part: MachinePart) -> Generator[tuple[str, MachinePart]]:
        for rule in self.rules:
            passed, part = rule.filter(part)
            if passed is not None:
                yield rule.destination, passed
    

class System:
    ACCEPT = 'A'
    REJECT = 'R'

    def __init__(self, workflows: Iterable[Workflow]):
        self.__wf_map = {w.id : w for w in workflows}

    def accept(self, part: MachinePart, start='in') -> bool:
        id = start
        while True:
            workflow = self.__wf_map[id]
            if (id := workflow.process(part)) in (self.ACCEPT, self.REJECT):
                return id == self.ACCEPT

    def count(self, min_rating, max_rating, start='in') -> int:
        queue = deque([(start, MachinePart(*[Interval(min_rating, max_rating)] * 4))])
        possibilities = 0
        while queue:
            id, part = queue.popleft()
            if id == self.ACCEPT:
                possibilities += part.possibilities
                continue
            queue.extend((i, p) for i, p in self.__wf_map[id].filter(part) if i != self.REJECT)
        return possibilities
    

@aoc.register(__file__)
def answers():
    workflows, parts = aoc.read_chunks()
    workflows = map(Workflow.from_string, workflows.splitlines())
    parts = map(MachinePart.from_string, parts.splitlines())

    system = System(workflows)
    yield sum(p.rating for p in parts if system.accept(p))
    yield system.count(min_rating=1, max_rating=4000)

if __name__ == '__main__':
    aoc.run()
