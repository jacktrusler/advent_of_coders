from __future__ import annotations
import aoc
from aoc.utils import adjacent_points
from collections import deque, defaultdict
from dataclasses import dataclass, field
from enum import Enum
import functools
import heapq
import numpy as np
from typing import Generator, Iterator


class Amphipod(Enum):
    AMBER  = 'A', 1
    BRONZE = 'B', 10
    COPPER = 'C', 100
    DESERT = 'D', 1000

    def __new__(cls, *values):
        obj = object.__new__(cls)
        for other_val in values[1:]:
            cls._value2member_map_[other_val] = obj
        obj._value_ = values[0]
        obj._values = values
        return obj
    
    @property
    def char(self) -> str:
        return self._values[0]
    
    @property
    def energy(self) -> int:
        return self._values[1]


class Burrow:
    @dataclass(frozen=True)
    class State:
        amphipods: set[tuple[aoc.Point, Amphipod]] = field(default_factory=set)
        effort: int = 0
        prev_moved: aoc.Point = None
        completed: set[aoc.Point] = field(default_factory=set)

        def __post_init__(self):
            super().__setattr__('amphipods', frozenset(self.amphipods))

        @functools.cache
        def __getitem__(self, idx: aoc.Point | Amphipod) -> Amphipod | set[aoc.Point]:
            match idx:
                case aoc.Point():
                    try:
                        return next(x[1] for x in self.amphipods if x[0] == idx)
                    except StopIteration:
                        raise IndexError
                case Amphipod():
                    return {x[0] for x in self.amphipods if x[1] == idx}

        def __hash__(self):
            return hash(self.amphipods)
        
        def __eq__(self, other: Burrow.State) -> bool:
            return self.amphipods == other.amphipods
        
        def __lt__(self, other: Burrow.State) -> bool:
            return self.effort < other.effort
        
        def __iter__(self) -> Iterator[tuple[aoc.Point, Amphipod]]:
            return iter(self.amphipods)
        

    def __init__(self, room_chart: list[str]):
        max_len = max(len(line) for line in room_chart)
        grid = np.array([list(x + ' ' * (max_len - len(x))) for x in room_chart])

        amphipod_values = [a.char for a in Amphipod]
        amphipods = {(p, Amphipod(grid[p.y][p.x])) for p in aoc.np.points(np.isin(grid, amphipod_values))}
        self.walls = set(aoc.np.points(grid == '#'))

        rooms = set(x[0] for x in amphipods)
        room_xs = sorted(set(p.x for p in rooms))
        self.targets = {a: [p for p in sorted(rooms, key=lambda x: x.y, reverse=True) if p.x == x] for a, x in zip(Amphipod, room_xs)}

        completed = set()
        for a in Amphipod:
            t_rooms = self.targets[a]
            for t_room in t_rooms:
                if (t_room, a) in amphipods:
                    completed.add(t_room)
                else:
                    break
        self.initial_state = Burrow.State(amphipods=amphipods, completed=completed)

        self.hallway = set(aoc.np.points(grid == '.'))
        self.landings = set(p for p in self.hallway if p.x not in room_xs)

    @functools.cache
    def _path(self, start: aoc.Point, target: aoc.Point) -> set[aoc.Point]:
        queue = deque([(start, set())])
        while queue:
            p, visited = queue.popleft()
            visited = visited | {p}
            if p == target:
                return visited - {start}
            for adj in (set(adjacent_points(p)) - (visited | self.walls)):
                queue.append((adj, visited))

    def _targets(self, state: Burrow.State, point: aoc.Point, amphipod: Amphipod) -> Generator[aoc.Point]:
        target_rooms = self.targets[amphipod]
        occupied = set(x[0] for x in state)

        for room in sorted(target_rooms, key=lambda p: p.y, reverse=True):
            try:
                a = state[room]
            except IndexError:
                if not occupied & self._path(point, room):
                    yield room
                break

            if a != amphipod:
                break

        if point not in self.hallway:
            yield from (x for x in self.landings if not (occupied & self._path(point, x)))

    def _possibilities(self, state: Burrow.State) -> Generator[Burrow.State]:
        for p, a in state:
            if p == state.prev_moved or p in state.completed:
                continue
            for new_p in self._targets(state, p, a):
                yield Burrow.State(
                    amphipods=state.amphipods - {(p, a)} | {(new_p, a)},
                    effort=state.effort + (self.distance(p, new_p) * a.energy),
                    prev_moved=new_p,
                    completed=state.completed if not new_p in self.targets[a] else state.completed | {new_p}
                )

    def distance(self, a: aoc.Point, b: aoc.Point) -> int:
        if a.x == b.x:
            return abs(a.y - b.y)
        hallway_y = next(iter(self.hallway)).y
        return (a.y - hallway_y) + (b.y - hallway_y) + abs(a.x - b.x)

    def estimate(self, state: Burrow.State) -> int:
        estimate = state.effort
        for a in Amphipod:
            current, targets = state[a], set(self.targets[a])
            remaining = tuple(targets - current), tuple(current - targets)
            for p1, p2 in zip(*remaining):
                estimate += self.distance(p1, p2) * a.energy
        return estimate

    def organize(self) -> Burrow.State:
        stack = []
        heapq.heappush(stack, (0, self.initial_state))
        visited = set()
        total = sum(len(v) for v in self.targets.values())

        while stack:
            _, state = heapq.heappop(stack)
            if len(state.completed) == total:
                return state
            visited.add(state)

            possible_states = set(self._possibilities(state))
            for new_state in set(possible_states) - visited:
                heapq.heappush(stack, (self.estimate(new_state), new_state))


@aoc.register(__file__)
def answers():
    data = aoc.read_lines('small')
    burrow1 = Burrow(data)
    yield burrow1.organize().effort
    
    # added_rooms = ['  #D#C#B#A#', '  #D#B#A#C#']
    # burrow2 = Burrow(data[:3] + added_rooms + data[3:])
    # yield burrow2.organize().effort

if __name__ == '__main__':
    aoc.run()
