from time import perf_counter_ns
from collections import deque
from operator import itemgetter


def outline(x: int, y: int, visited: set, search: set):
    results = set()
    for (a, b) in {(max(x-1, 0), y), (min(x+1, 6), y), (x, max(y-1, 0))} - visited:
        visited.add((a, b))
        if (a, b) in search:
            results.add((a, b))
        else:
            results.update(outline(a, b, visited, search))
    return results


def move(rock: set, x: int, y: int, obstacles: set = None):
    new_points = set()
    obstacles = set() if obstacles is None else obstacles
    for px, py in rock:
        new_x = px + x
        new_y = py + y
        if (new_x, new_y) in obstacles or not 0 <= new_x <= 6 or new_y <= 0:
            raise ValueError
        new_points.add((new_x, new_y))
    return new_points


def sim(jets: list, max_rocks: int):
    rocks = deque((
        {(0, 0), (1, 0), (2, 0), (3, 0)},
        {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
        {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
        {(0, 0), (0, 1), (0, 2), (0, 3)},
        {(0, 0), (1, 0), (0, 1), (1, 1)}
    ))
    # iterate over the jets to force a state check whenever we loop the list of jets.
    iter_jet = iter(jets)
    obstacles = set()
    total_height = 0
    rock_height_changes = list()
    states = dict()
    for i in range(max_rocks):
        rock = {(x+2, y + total_height + 4) for x, y in rocks[0]}
        rocks.rotate(-1)
        falling = True
        while falling:
            try:
                jet = next(iter_jet)
            except StopIteration:
                # subtract total height to normalize the values and make the states comparable.
                tower_state = frozenset((x, y-total_height) for x, y in outline(0, total_height+1, set(), obstacles))
                rock_state = frozenset((x, y-total_height) for x, y in rock)
                state = (tower_state, rock_state)
                if state in states:
                    # If we've seen this state before, we can calculate the total height instead of running the rest
                    # of the simulation.
                    prev_i, prev_height = states[state]
                    height_adjustment = (max_rocks - i) // (i - prev_i)
                    post_cycle_rocks = sum(rock_height_changes[prev_i:prev_i + (max_rocks - i) % (i - prev_i)])
                    return total_height + ((total_height - prev_height) * height_adjustment) + post_cycle_rocks
                states[state] = (i, total_height)
                iter_jet = iter(jets)
                jet = next(iter_jet)

            # move left/right
            try:
                rock = move(rock, jet, 0, obstacles)
            except ValueError:
                pass

            # move down and handle settling
            try:
                rock = move(rock, 0, -1, obstacles)
            except ValueError:
                obstacles.update(rock)
                rock_height = max(rock, key=itemgetter(1))[1]
                # track rock height changes to assist with the end-of-cycle calculations.
                rock_height_changes.append(max(rock_height - total_height, 0))
                if rock_height > total_height:
                    total_height = rock_height
                falling = False
    return total_height


def solve(raw_input: str):
    jets = [-1 if c == '<' else 1 for c in raw_input.strip()]
    a = sim(jets, 2022)
    b = sim(jets, 1000000000000)
    return a, b


def main():
    with open('./day17_input.txt', mode='r') as f:
        problem_input = f.read()
    start_time = perf_counter_ns()
    a, b = solve(problem_input)
    end_time = perf_counter_ns()
    elapsed_ms = round((end_time - start_time) / 1000000, 3)
    print(f'A: {a}')
    print(f'B: {b}')
    print(f'Elapsed time: {elapsed_ms} ms')


if __name__ == '__main__':
    main()
