import aoc
from aoc.grid import Point, Grid, Direction
import functools


class TopographicMap(Grid[int]):
    def __post_init__(self):
        self.trails = functools.cache(self.trails)

    def trails(self, p: Point) -> tuple[Point, int]:
        if (v := self[p]) == 9:
            return {p}, 1
        
        ends, unique = set(), 0
        for d in Direction:
            a = p + d.movement
            if not self.binds(a) or self[a] != v + 1:
                continue
            _ends, _unique = self.trails(a)
            ends, unique = (ends | _ends), unique + _unique
        return ends, unique
    
    def score(self, p: Point) -> int:
        return len(self.trails(p)[0])
    
    def rating(self, p: Point) -> int:
        return self.trails(p)[1]

@aoc.register(__file__)
def answers():
    topographic_map = TopographicMap(aoc.read_grid(), dtype=int)
    trailheads = tuple(topographic_map.find(0))
    
    yield sum(topographic_map.score(t) for t in trailheads)
    yield sum(topographic_map.rating(t) for t in trailheads)

if __name__ == '__main__':
    aoc.run()
