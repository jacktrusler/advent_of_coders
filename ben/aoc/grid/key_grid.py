from __future__ import annotations
from abc import ABC
from aoc.grid.point import Point
from aoc.grid.grid import BaseGrid
from collections import defaultdict
import re
from typing import Generic, TypeVar


T = TypeVar('T')
class KeyGrid(BaseGrid, Generic[T], ABC):
    class Field:
        def __init__(self, key):
            self.key = key

    fields: dict[str, str] = None
    ignore: str = None

    def __init__(self, data: str):
        if self.fields is None and self.ignore is None:
            raise TypeError('Fields or Ignore must be declared for a KeyGrid')
        self.__points: dict[str, set[Point]] = defaultdict(set)

        if self.fields is not None:
            values = set(self.fields.values())
            value_map = {v: k for k, v in self.fields.items()}
        elif self.ignore is not None:
            self.ignore += '\n'
            values = set(data) - set(self.ignore)
            value_map = {v: v for v in values}
        
        width = data.index('\n')
        line_length = width + 1
        height = len(data.splitlines())

        def _per_match(m: re.Match):
            y, x = divmod(m.start(), line_length)
            key = value_map[m.group(0)]
            self.__points[key].add(Point(x, y))
        escaped = '.^$*+?()[{|-]\\'
        regex = rf'[{"|".join(x if x not in escaped else f"{chr(92)}{x}" for x in values)}]'
        [_per_match(m) for m in re.finditer(regex, data)]

        super().__init__(width, height)

    def __str__(self):
        return str(dict(self.__points))

    def __getattr__(self, name: str):
        if name not in self.__points:
            raise AttributeError
        return self.__points[name]

    def __getitem__(self, key: str) -> set[Point]:
        if key not in self.__points:
            raise KeyError
        return self.__points[key]
    
    def keys(self): return self.__points.keys()
    def values(self): return self.__points.values()
    def items(self): return self.__points.items()
    

class TestGrid(KeyGrid):
    fields = {'test': '^'}
    

if __name__ == '__main__':
    test_str = '...^\n.^..\n^^..\n....'
    kg = TestGrid(test_str)
    print(kg)
    print(kg.test)