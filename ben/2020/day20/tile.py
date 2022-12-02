from __future__ import annotations
import numpy as np
from numpy.typing import NDArray
import re

try:
    from location import Direction
except ImportError:
    from .location import Direction


class Tile:
    Edge = tuple[str]

    def __init__(self, id: int, content: NDArray):
        self.id = id
        self._content = content

        self._edges: dict[Tile.Edge, Direction] = {
            tuple(self._content[0]): Direction.ABOVE,
            tuple(self._content[:,-1]): Direction.RIGHT,
            tuple(self._content[-1][::-1]): Direction.BELOW,
            tuple(self._content[:,0][::-1]): Direction.LEFT
        }

    def __str__(self):
        content_str = '\n'.join([''.join([char for char in line]) for line in self._content])
        return f'Tile {self.id}:\n{content_str}'

    def __repr__(self):
        return f'Tile({self.id})'

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other: Tile):
        return self.id == other.id

    @property
    def content(self) -> str:
        return self._content[1:-1, 1:-1]

    def edges(self, include_flipped=False) -> set[Tile.Edge]:
        edges = set(self._edges.keys())
        if not include_flipped:
            return edges
        return edges | {edge[::-1] for edge in edges}

    def direction_of_edge(self, edge: Tile.Edge) -> Direction:
        return self._edges[edge]

    def matching_edge(self, other: Tile) -> Tile.Edge | None:
        try:
            return list(self.edges() & other.edges(include_flipped=True))[0]
        except IndexError:
            None

    def attach(self, other: Tile) -> tuple[Tile, Direction]:
        edge = self.matching_edge(other)
        if edge in other.edges():
            other = other.flip()
        src_dir = self.direction_of_edge(edge)
        other_dir = other.direction_of_edge(edge[::-1])
        other = other.rotate((src_dir + 2 - other_dir).value)
        return other, src_dir

    def rotate(self, n: int=1, clockwise=True) -> Tile:
        return Tile(self.id, np.rot90(self._content, k=-1*n if clockwise else 1*n))
        
    def flip(self) -> Tile:
        return Tile(self.id, np.flip(self._content, axis=1))

    @staticmethod
    def from_string(tile_str: str) -> Tile:
        lines = tile_str.splitlines()
        id = int(re.match(r'Tile (.*):', lines[0])[1])
        shape = np.array([list(x) for x in lines[1:]])
        return Tile(id=id, content=shape)
