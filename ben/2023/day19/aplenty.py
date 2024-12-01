from __future__ import annotations
import aoc
from aoc.utils import Interval
from collections import defaultdict, deque
from dataclasses import dataclass, replace
from operator import lt, gt
from math import prod
import re
from typing import Iterable, Callable


@dataclass
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


class Workflow:
    @dataclass(frozen=True)
    class Rule:
        result: str
        category: str = None
        operation: Callable = None
        value: int = None

        @classmethod
        def from_string(cls, rule: str) -> Workflow.Rule:
            if ':' not in rule:
                return cls(rule)
            m = re.match(r'(?P<category>.*)(?P<cond>[<>])(?P<value>\d+):(?P<result>.*)', rule).groupdict()
            op = lt if m['cond'] == '<' else gt
            return cls(m['result'], m['category'], op, int(m['value']))

        def process(self, part: MachinePart) -> bool:
            if self.category is None:
                return True
            return self.operation(part[self.category].start, self.value)
        
        def filter(self, part: MachinePart) -> tuple[MachinePart, MachinePart]:
            if self.category is None:
                return part, None
            if not (v := part[self.category]) & self.value:
                return None, part
            
            below = Interval(v.start, self.value-1 if self.operation == lt else self.value)
            above = Interval(self.value + 1 if self.operation == gt else self.value, v.end)
            passed = below if self.operation == lt else above
            failed = above if self.operation == lt else below
            return part.replace(self.category, passed), part.replace(self.category, failed)
            

    def __init__(self, id: int, rules: list[str]):
        self.id = id
        self.rules = list(map(Workflow.Rule.from_string, rules))

    @classmethod
    def from_string(cls, workflow: str) -> Workflow:
        id, rules = re.match(r'(?P<id>.*){(?P<rules>.*)}', workflow).groups()
        return cls(id, rules.split(','))

    def process(self, part: MachinePart) -> str:
        for rule in self.rules:
            if rule.process(part):
                return rule.result

    def filter(self, part: MachinePart) -> dict[str, list[MachinePart]]:
        results = defaultdict(list)
        for rule in self.rules:
            passed, part = rule.filter(part)
            if passed is not None:
                results[rule.result].append(passed)
        return results
    

class System:
    def __init__(self, workflows: Iterable[Workflow]):
        self.__wf_map = {w.id : w for w in workflows}

    def accept(self, part: MachinePart, start='in') -> bool:
        workflow = self.__wf_map[start]
        while True:
            if (result := workflow.process(part)) in 'AR':
                return result == 'A'
            workflow = self.__wf_map[result]

    def count(self, min_rating, max_rating, start='in') -> int:
        all_parts = MachinePart(*[Interval(min_rating, max_rating)] * 4)
        queue = deque([(self.__wf_map[start], all_parts)])
        possibilities = 0
        while queue:
            workflow, part = queue.popleft()
            results = workflow.filter(part)

            for id, parts in results.items():
                if id == 'A':
                    possibilities += sum(p.possibilities for p in parts)
                if id in 'AR':
                    continue
                queue.append((self.__wf_map[id], parts[0]))
        return possibilities
    

@aoc.register(__file__)
def answers():
    workflows, parts = aoc.read_chunks()
    workflows = map(Workflow.from_string, workflows.splitlines())
    parts = list(map(MachinePart.from_string, parts.splitlines()))

    system = System(workflows)
    yield sum(p.rating for p in parts if system.accept(p))
    yield system.count(min_rating=1, max_rating=4000)

if __name__ == '__main__':
    aoc.run()
