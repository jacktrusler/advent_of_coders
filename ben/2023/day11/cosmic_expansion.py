from __future__ import annotations
import aoc
import itertools
import numpy as np


class Universe:
    def __init__(self, input: list[list[str]]):
        grid = np.array(input)
        self.galaxies = set(aoc.np.points(grid == '#'))
        x_vals = {gal[0] for gal in self.galaxies}
        y_vals = {gal[1] for gal in self.galaxies}
        self.expanded_rows = set(range(grid.shape[0])) - y_vals
        self.expanded_cols = set(range(grid.shape[1])) - x_vals

    def distance(self, galaxy_a: aoc.Point, galaxy_b: aoc.Point, expansion: int = 2) -> int:
        d = abs(galaxy_a[0] - galaxy_b[0]) + abs(galaxy_a[1] - galaxy_b[1])
        x_vals = sorted((galaxy_a[0], galaxy_b[0]))
        y_vals = sorted((galaxy_a[1], galaxy_b[1]))
        expanded = sum(1 for x in self.expanded_cols if x_vals[0] < x < x_vals[1])
        expanded += sum(1 for y in self.expanded_rows if y_vals[0] < y < y_vals[1])
        expanded *= (expansion - 1)
        return d + expanded


@aoc.register(__file__)
def answers():
    universe = Universe(aoc.read_grid())
    yield sum(universe.distance(a, b) for a, b in itertools.combinations(universe.galaxies, 2))
    yield sum(universe.distance(a, b, 1000000) for a, b in itertools.combinations(universe.galaxies, 2))

if __name__ == '__main__':
    aoc.run()
