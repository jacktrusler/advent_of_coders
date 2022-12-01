from __future__ import annotations
import aoc
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import reduce
import itertools
import re


class Direction(Enum):
    NORTHEAST = 'ne'
    EAST = 'e'
    SOUTEAST = 'se'
    SOUTHWEST = 'sw'
    WEST = 'w'
    NORTHWEST = 'nw'

@dataclass(eq=True, frozen=True)
class Location:
    x: int
    y: int

    def move(self, dir: Direction) -> Location:
        match dir:
            case Direction.NORTHEAST: return Location(self.x+1, self.y+1)
            case Direction.EAST: return Location(self.x+2, self.y)
            case Direction.SOUTEAST: return Location(self.x+1, self.y-1)
            case Direction.SOUTHWEST: return Location(self.x-1, self.y-1)
            case Direction.WEST: return Location(self.x-2, self.y)
            case Direction.NORTHWEST: return Location(self.x-1, self.y+1)


def adjacent_tiles(tile: Location) -> set[Location]:
    return {tile.move(dir) for dir in Direction}

def check_black(black_tiles: set[Location], adjacents: set[Location]) -> bool:
    adjacent_blacks = len(adjacents & black_tiles)
    return adjacent_blacks == 0 or adjacent_blacks > 2

def process_day(black_tiles: set[Location]) -> set[Location]:
    adjacents = {tile: adjacent_tiles(tile) for tile in black_tiles}
    blacks_to_flip = {tile for tile, adj in adjacents.items() if check_black(black_tiles, adj)}

    adj_counter = Counter(list(itertools.chain.from_iterable(adjacents.values())))
    whites_to_flip = {tile for tile, n in adj_counter.items() if n == 2}

    return (black_tiles | whites_to_flip) - blacks_to_flip


def main():
    aoc.setup(__file__)
    lines = aoc.read_lines()
    delims = '|'.join(d.value for d in Direction)
    lines = [list(filter(None, re.split(f'({delims})', line))) for line in lines]

    origin = Location(0,0)
    flipped_tiles = [reduce(lambda x,y: x.move(Direction(y)), line, origin) for line in lines]
    flipped_tiles = Counter(flipped_tiles)
    state = {tile for tile, n in flipped_tiles.items() if n % 2 != 0}
    aoc.answer(1, len(state))

    for _ in range(100):
        state = process_day(state)
    aoc.answer(2, len(state))

if __name__ == '__main__':
    main()
