from __future__ import annotations
import aoc
from aoc.grid import Point, KeyGrid, Direction
from dataclasses import dataclass


class GuardMap(KeyGrid):
    obstacles = '#'
    guard = '^'

class InfiniteLoopError(Exception):
    pass

@dataclass(frozen=True)
class PatrolState:
    position: Point
    direction: Direction

    def move(self) -> PatrolState:
        return PatrolState(Point(self.position.x + self.direction.movement[0], self.position.y + self.direction.movement[1]), self.direction)
        return PatrolState(self.position.move(self.direction), self.direction)
    
    def turn(self) -> PatrolState:
        return PatrolState(self.position, self.direction.rotate())

def run_patrol(guard_map: GuardMap, new_obstacle: Point = None) -> set[PatrolState]:
    obstacles = set(guard_map.obstacles)
    if new_obstacle:
        obstacles.add(new_obstacle)

    state = PatrolState(list(guard_map.guard)[0], Direction.UP)
    visited = set([state])
    
    while True:
        next_state = state.move()
        if next_state.position in obstacles:
            state = state.turn()
            continue

        if not guard_map.binds(next_state.position):
            break

        if next_state in visited:
            raise InfiniteLoopError
        
        visited.add(next_state)
        state = next_state
    return visited

def check_for_loop(guard_map: GuardMap, new_obstacle: Point) -> bool:
    try:
        run_patrol(guard_map, new_obstacle)
    except InfiniteLoopError:
        return True
    return False

@aoc.register(__file__)
def answers():
    guard_map = GuardMap(aoc.read_data())

    patrol = run_patrol(guard_map)
    yield len({x.position for x in patrol})

    occupied = guard_map.obstacles | guard_map.guard
    all_points = {x.position for x in patrol} - occupied
    yield sum(check_for_loop(guard_map, p) for p in all_points)

if __name__ == '__main__':
    aoc.run()
