from __future__ import annotations
import aoc
from aoc.grid import Point, KeyGrid, Direction
from dataclasses import dataclass
import functools


class GuardMap(KeyGrid):
    fields = {
        'obstacles': '#',
        'guard': '^'
    }

class InfiniteLoopError(Exception):
    pass

def run_patrol(guard_map: GuardMap, obstacles: set[tuple[int, int]]) -> set[tuple[int, int]]:
    guard = list(guard_map.guard)[0]
    guard = Point(guard.x, guard.y)
    state = ((guard.x, guard.y), (0, -1))
    visited = {state}

    width, height = guard_map.width, guard_map.height
    
    while True:
        next_state = ((state[0][0] + state[1][0], state[0][1] + state[1][1]), state[1])
        if next_state[0] in obstacles:
            new_dir_x = 0 if state[1][0] != 0 else (1 if state[1][1] == -1 else -1)
            new_dir_y = 0 if state[1][1] != 0 else (1 if state[1][0] == 1 else -1)
            state = (state[0], (new_dir_x, new_dir_y))
            continue

        if not guard_map.binds(next_state[0]):
            break

        # if not (0 <= next_state[0][0] < width and 0 <= next_state[0][1] < height):
        #     break

        if next_state in visited:
            raise InfiniteLoopError
        
        visited.add((next_state))
        state = next_state
    return {x[0] for x in visited}

def check_for_loop(guard_map: GuardMap, obstacles: set[tuple[int, int]], new_obstacle: tuple[int, int]) -> bool:
    try:
        run_patrol(guard_map, obstacles | {new_obstacle})
    except InfiniteLoopError:
        return True
    return False

@aoc.register(__file__)
def answers():
    guard_map = GuardMap(aoc.read_data())
    obstacles = {(p.x, p.y) for p in guard_map.obstacles}
    p = list(guard_map.guard)[0]
    print(p)
    guard = Point(p.x, p.y)
    guard = (guard.x, guard.y)

    patrol = run_patrol(guard_map, obstacles)
    yield len(patrol)

    all_points = patrol - obstacles - {guard}
    yield sum(check_for_loop(guard_map, obstacles, p) for p in all_points)

if __name__ == '__main__':
    aoc.run()
