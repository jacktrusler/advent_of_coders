import aoc
from aoc.utils import pairwise
from collections import defaultdict
import math


TEST_CUBES = {
    'red': 12,
    'green': 13,
    'blue': 14
}

@aoc.register(__file__)
def answers():
    valid_game_total, power = 0, 0
    for i, game_log in enumerate(aoc.read_lines(), start=1):
        cube_counts = defaultdict(set)
        game_log = game_log.split(': ')[1].replace(',', '').replace(';', '').split(' ')
        
        for amount, color in pairwise(game_log):
            cube_counts[color].add(int(amount))
        max_cubes = {k: max(v) for k, v in cube_counts.items()}

        if all(v <= TEST_CUBES[k] for k, v in max_cubes.items()):
            valid_game_total += i
        power += math.prod(max_cubes.values())
    yield valid_game_total
    yield power

if __name__ == '__main__':
    aoc.run()
