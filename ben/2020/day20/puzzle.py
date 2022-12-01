from collections import defaultdict, deque
import itertools
import numpy as np
from numpy.typing import NDArray

try:
    from image import Image
    from location import Direction, Location
    from tile import Tile
except ImportError:
    from .image import Image
    from .location import Direction, Location
    from .tile import Tile


class Puzzle:
    def __init__(self, tiles: list[Tile]):
        puzzle_len = int(len(tiles) ** 0.5)
        self._layout: NDArray = np.full(shape=(puzzle_len, puzzle_len), fill_value=None, dtype=object)
        self._build_puzzle(tiles)

    def __getitem__(self, loc: Location) -> Tile:
        return self._layout[loc.y][loc.x]

    def __setitem__(self, loc: Location, tile: Tile):
        self._layout[loc.y][loc.x] = tile

    def __str__(self):
        content_str = '\n'.join([' '.join([str(tile.id) for tile in row]) for row in self._layout])
        return content_str

    @property
    def image(self) -> Image:
        all_rows = [np.hstack([t.content for t in row]) for row in self._layout]
        content = np.vstack(all_rows)
        return Image(content)

    def corners(self) -> list[Tile]:
        return [self[Location(0, 0)], self[Location(-1, 0)], self[Location(0, -1)], self[Location(-1, -1)]]

    def _create_match_dict(self, tiles: list[Tile]) -> dict[Tile, set[Tile]]:
        match_dict: defaultdict[Tile, set[Tile]] = defaultdict(set)
        for tile1, tile2 in itertools.combinations(tiles, 2):
            if tile1.matching_edge(tile2) is not None:
                match_dict[tile1].add(tile2)
                match_dict[tile2].add(tile1)
        return match_dict

    def _top_left(self, match_dict: dict[Tile, set]) -> Tile:
        top_left = next(tile for tile, matches in match_dict.items() if len(matches) == 2)
        top_left_matches = {top_left.matching_edge(match) for match in match_dict[top_left]}
        edge_dirs = {top_left.direction_of_edge(match) for match in top_left_matches}
        if edge_dirs == {Direction.ABOVE, Direction.RIGHT}: top_left = top_left.rotate()
        elif edge_dirs == {Direction.BELOW, Direction.LEFT}: top_left = top_left.rotate(clockwise=False)
        elif edge_dirs == {Direction.LEFT, Direction.ABOVE}: top_left = top_left.rotate(n=2)
        return top_left

    def _build_puzzle(self, tiles: list[Tile]):
        match_dict = self._create_match_dict(tiles)

        # Place all of the tiles
        tiles_to_place = deque([(self._top_left(match_dict), Location(0, 0))])
        while tiles_to_place:
            tile, loc = tiles_to_place.popleft()
            try:
                matches = match_dict.pop(tile)
            except KeyError:
                continue
            self[loc] = tile
            
            for match in matches:
                if match not in match_dict:
                    continue
                match, direction = tile.attach(match)
                new_loc = loc.move(direction)
                tiles_to_place.append((match, new_loc))
