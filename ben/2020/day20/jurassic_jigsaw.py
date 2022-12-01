import aoc
from math import prod

try:
    from tile import Tile
    from puzzle import Puzzle
except ImportError:
    from .tile import Tile
    from .puzzle import Puzzle


@aoc.register(__file__)
def answers():
    tiles = [Tile.from_string(chunk) for chunk in aoc.read_chunks()]

    puzzle = Puzzle(tiles)
    yield prod(t.id for t in puzzle.corners())

    image = puzzle.image
    points = set.union(*[x.points for x in image.sea_monsters()])
    yield image.count_hash() - len(points)

if __name__ == '__main__':
    aoc.run()
