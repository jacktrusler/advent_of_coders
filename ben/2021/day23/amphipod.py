from __future__ import annotations
import aoc
from aoc.utils import pairwise
from dataclasses import dataclass, field
from enum import Enum
import heapq
import numpy as np


class Amphipod(Enum):
    AMBER = 1
    BRONZE = 10
    COPPER = 100
    DESERT = 1000

class Burrow:
    @dataclass(frozen=True)
    class State:
        amphipods: dict[aoc.Point, Amphipod] = field(default_factory=dict)
        effort: int = 0
        estimate: int = 0

        def __hash__(self):
            return hash(self.amphipods)

        def __lt__(self, other: Burrow.State) -> bool:
            return self.estimate < other.estimate

    def __init__(self, room_chart: str):
        lines = room_chart.splitlines()
        max_len = max(len(line) for line in lines)
        grid = np.array([list(x + ' ' * (max_len - len(x))) for x in lines])

        amphipods = {p: grid[p.y][p.x] for p in aoc.np.points(np.isin(grid, ['A', 'B', 'C', 'D']))}
        self.rooms = set(amphipods.keys())
        self.hallway = set(aoc.np.points(grid == '.'))
        self.initial_state = Burrow.State(amphipods)

        sorted_rooms = sorted(self.rooms, key=lambda p: (p.x, p.y))
        self.target_rooms = {a: rooms for a, rooms in zip(Amphipod, pairwise(sorted_rooms))}

    def path_to(self, a: aoc.Point, b: aoc.Point) -> set[aoc.Point]:
        if a.x == b.x:
            return 

    def distance(self, a: aoc.Point, b: aoc.Point) -> int:
        if a.x == b.x:
            return abs(a.y - b.y)
        
        hallway_y = next(iter(self.hallway)).y
        return (a.y - hallway_y) + (b.y - hallway_y) + abs(a.x - b.x)            

    def complete(self, state: Burrow.State) -> bool:
        for a, points in self.target_rooms.items():
            for p in points:
                try:
                    if state.amphipods[p] != a:
                        return False
                except KeyError:
                    return False
        return True

    def estimate(self, state: Burrow.State) -> int:
        estimate = 0
        for a in Amphipod:
            for p in state.amphipods[a]:
                if p in self.target_rooms[a]:
                    continue
                estimate += a.value * self.distance(p, self.target_rooms[a][0])
        return estimate

    def valid_moves(self, state: Burrow.State) -> set[Burrow.State]:
        occupied = set(state.amphipods.keys())
        unoccupied = (self.hallway | self.rooms) - occupied
        for point, a in state.amphipods.items():
            if point in 

    def organize(self) -> int:
        stack = []
        heapq.heappush(stack, self.initial_state)
        visited = set()

        while stack:
            state: Burrow.State = heapq.heappop(stack)
            if self.complete(state):
                return
            visited.add(state)

            for new_state in self.valid_moves(state) - visited:
                heapq.heappush(stack, new_state)


@aoc.register(__file__)
def answers():
    rooms = Burrow(aoc.read_data('small'))

if __name__ == '__main__':
    aoc.run()
