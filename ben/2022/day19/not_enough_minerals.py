from __future__ import annotations
import aoc
from collections import deque
from dataclasses import dataclass, field
from math import prod
import re
from typing import ClassVar, Generator


@dataclass(frozen=True, eq=True)
class Resources:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    keys: ClassVar[tuple[str]] = ('ore', 'clay', 'obsidian', 'geode')

    def items(self) -> Generator[tuple[str, int]]:
        for resource in self.keys:
            yield resource, getattr(self, resource)

    def values(self) -> Generator[int]:
        for resource in self.keys:
            yield getattr(self, resource)

    def __getitem__(self, k: str):
        return getattr(self, k)

    def __add__(self, other: Resources) -> Resources:
        return Resources(self.ore + other.ore, self.clay + other.clay, self.obsidian + other.obsidian, self.geode + other.geode)

    def __sub__(self, other: Resources) -> Resources:
        return Resources(self.ore - other.ore, self.clay - other.clay, self.obsidian - other.obsidian, self.geode - other.geode)

    def __ge__(self, other: Resources) -> bool:
        return self.ore >= other.ore and self.clay >= other.clay and self.obsidian >= other.obsidian and self.geode >= other.geode

    @classmethod
    def max(cls, *args) -> Resources:
        retval = {k: 0 for k in cls.keys}
        for r in args:
            retval['ore'] = max(retval['ore'], r.ore)
            retval['clay'] = max(retval['clay'], r.clay)
            retval['obsidian'] = max(retval['obsidian'], r.obsidian)
            retval['geode'] = max(retval['geode'], r.geode)
        return Resources(**retval)

@dataclass(frozen=True, eq=True)
class State:
    time: int
    resources: Resources = field(default=Resources())
    bots: Resources = field(default=Resources(ore=1))

    def collect(self) -> State:
        return State(
            time = self.time - 1,
            resources = self.resources + self.bots,
            bots = self.bots,
        )

    def build(self, bot_type: str, cost: Resources) -> State:
        return State(
            time = self.time,
            resources = self.resources - cost,
            bots = self.bots + Resources(**{bot_type: 1}),
        )

    def best_case(self, resource) -> int:
        return self.resources[resource] + self.bots[resource] * (self.time + 1) + self.time * (self.time + 1) // 2

@dataclass
class Blueprint:
    id: int
    costs: dict[str, Resources] = field(default_factory=dict)

    def can_build(self, state: State) -> Generator[str]:
        for resource, cost in self.costs.items():
            if state.resources >= cost:
                yield resource

    def max_geodes(self, time: int) -> int:
        max_resource_rq = Resources.max(*self.costs.values())
        queue = deque([(State(time=time), set())])
        visited = set()
        _max = 0

        while queue:
            state, avoided = queue.pop()
            if state in visited:
                continue
            visited.add(state)

            if state.time <= 0:
                _max = max(_max, state.resources.geode)
                continue
            post_collect = state.collect()
            can_build = set()

            if post_collect.best_case('geode') < _max:
                continue

            if post_collect.best_case('obsidian') < self.costs['geode'].obsidian or post_collect.best_case('ore') < self.costs['geode'].ore:
                _max = max(_max, post_collect.resources.geode + post_collect.bots.geode * post_collect.time)
                continue

            for bot_type in self.can_build(state):
                can_build.add(bot_type)
                if bot_type != 'geode' and state.bots[bot_type] >= max_resource_rq[bot_type] or bot_type in avoided:
                    continue
                queue.append((post_collect.build(bot_type, self.costs[bot_type]), set()))

            if (state.resources.ore < max_resource_rq.ore) or \
                (state.bots.clay > 0 and state.resources.clay < max_resource_rq.clay) or \
                    (state.bots.obsidian > 0 and state.resources.obsidian < max_resource_rq.obsidian):
                queue.append((post_collect, can_build))
        
        return _max

    @staticmethod
    def from_string(bp_str: str) -> Blueprint:
        re_str = r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. '
        re_str += r'Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.'
        m = tuple(map(int, re.match(re_str, bp_str).groups()))
        return Blueprint(id=m[0], costs={
            'ore': Resources(m[1], 0, 0, 0),
            'clay': Resources(m[2], 0, 0, 0),
            'obsidian': Resources(m[3], m[4], 0, 0),
            'geode': Resources(m[5], 0, m[6], 0)
        })

@aoc.register(__file__)
def answers():
    blueprints = [Blueprint.from_string(line) for line in aoc.read_lines()]

    yield sum(bp.id * bp.max_geodes(time=24) for bp in blueprints)
    yield prod(bp.max_geodes(time=32) for bp in blueprints[:3])

if __name__ == '__main__':
    aoc.run()
