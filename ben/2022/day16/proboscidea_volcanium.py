from __future__ import annotations
import aoc
from collections import defaultdict, deque
from dataclasses import dataclass, field
import itertools
import re
from typing import ClassVar, Generator


@dataclass
class Valve:
    name: str
    flow_rate: int = field(compare=False, repr=False)
    tunnels: frozenset[str] = field(repr=False, default_factory=frozenset, compare=False)
    _ALL: ClassVar[dict[str, Valve]] = {}

    @classmethod
    def get(cls, name: str) -> Valve:
        return Valve._ALL[name]

    def __hash__(self):
        return hash(self.name)

    def __post_init__(self):
        Valve._ALL[self.name] = self

    def distance(self, other: Valve) -> int:
        queue = deque([(0, self)])
        visited = set()

        while queue:
            distance, valve = queue.popleft()

            if valve == other:
                return distance
            if valve.name in visited:
                continue
            visited.add(valve.name)

            for adj in valve.tunnels - visited:
                adj_val = Valve._ALL[adj]
                queue.append((distance + 1, adj_val))

    def paths(self, dists: dict, targets: set[Valve], time: int, chosen={}) -> Generator[Path]:
        for target in targets:
            if (new_t := time - dists[self][target] - 1) < 2:
                continue
            _chosen = chosen | {target: new_t}
            yield from target.paths(dists, targets - {target}, new_t, _chosen)
        yield chosen

    @staticmethod
    def from_string(valve_str: str) -> Valve:
        m = re.match(r'Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)', valve_str).groups()
        tunnels = m[2].split(', ')
        return Valve(name=m[0], flow_rate=int(m[1]), tunnels=set(tunnels))

Path = dict[Valve, int]

def shortest_paths(valves: set[Valve]):
    dists = defaultdict(dict)
    for v1, v2 in itertools.combinations(valves, 2):
        d = v1.distance(v2)
        dists[v1][v2] = d
        dists[v2][v1] = d
    return dists

def pressure(path: Path) -> int:
    return sum(v.flow_rate * t for v, t in path.items())


@aoc.register(__file__)
def answers():
    valves = [Valve.from_string(x) for x in aoc.read_lines()]

    target_valves = {v for v in valves if v.flow_rate > 0}
    path_graph = shortest_paths(target_valves | {Valve.get('AA')})
    yield max([pressure(p) for p in Valve.get('AA').paths(path_graph, target_valves, time=30)])

    max_pressure = defaultdict(lambda: -1)
    for p in Valve.get('AA').paths(path_graph, target_valves, time=26):
        k = frozenset(p)
        max_pressure[k] = max(max_pressure[k], pressure(p))
    yield max([pres1 + pres2 for (path1, pres1), (path2, pres2) in itertools.combinations(max_pressure.items(), 2) if not path1 & path2])

if __name__ == '__main__':
    aoc.run()
