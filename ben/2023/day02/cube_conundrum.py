import aoc
from aoc.utils import pairwise
from collections import defaultdict
from math import prod


TEST_CUBES = {'red': 12, 'green': 13, 'blue': 14}

@aoc.register(__file__)
def answers():
    valid_game_total, power = 0, 0
    for i, game_log in enumerate(aoc.read_lines(), start=1):
        game_log = game_log.split(':')[1].replace(',', '').replace(';', '').split()
        max_cubes = defaultdict(int)
        
        for amount, color in pairwise(game_log):
            max_cubes[color] = max(int(amount), max_cubes[color])

        if all(v <= TEST_CUBES[k] for k, v in max_cubes.items()):
            valid_game_total += i
        power += prod(max_cubes.values())
    yield valid_game_total
    yield power

if __name__ == '__main__':
    aoc.run()
