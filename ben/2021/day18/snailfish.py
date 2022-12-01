from __future__ import annotations
from abc import ABC, abstractmethod
import aoc
from copy import deepcopy
from dataclasses import dataclass, field
import itertools
import math
import uuid


@dataclass
class SnailfishNumber(ABC):
    parent: Pair | None = field(default=None, init=False, repr=False)
    uid: uuid.UUID = field(init=False, repr=False, default_factory=lambda: str(uuid.uuid4()))

    def __add__(self, other: SnailfishNumber) -> SnailfishNumber:
        return Pair(deepcopy(self), deepcopy(other)).reduce()

    def __radd__(self, other) -> SnailfishNumber:
        if other == 0:
            return self
        return self.__add__(other)

    def __eq__(self, other: SnailfishNumber):
        return self.uid == other.uid

    @abstractmethod
    def leftmost(self) -> Literal: pass

    @abstractmethod
    def rightmost(self) -> Literal: pass

    @abstractmethod
    def explode(self) -> bool: pass

    @abstractmethod
    def split(self) -> bool: pass

    @abstractmethod
    def magnitude(self) -> int: pass

    def position(self) -> int | None:
        try:
            if self == self.parent.first:
                return 0
            if self == self.parent.second:
                return 1
        except AttributeError:
            return None

    def left(self) -> Literal | None:
        if self.position() == 1:
            return self.parent.first.rightmost()
        try:
            return self.parent.left().rightmost()
        except AttributeError:
            return None

    def right(self) -> Literal | None:
        if self.position() == 0:
            return self.parent.second.leftmost()
        try:
            return self.parent.right().leftmost()
        except AttributeError:
            return None

    def reduce(self) -> SnailfishNumber:
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            break
        return self

    @staticmethod
    def from_string(num_str: str) -> SnailfishNumber:
        while num_str[0] in [']', ',']:
            num_str = num_str[1:]

        if num_str[0].isdigit():
            val = num_str[0]
            retval = Literal(int(val))
            num_str = num_str[1:]
            return retval, num_str

        num_str = num_str[1:len(num_str)]
        first, num_str = SnailfishNumber.from_string(num_str)
        second, num_str = SnailfishNumber.from_string(num_str)
        return Pair(first, second), num_str

@dataclass
class Literal(SnailfishNumber):
    value: int

    def __repr__(self):
        return f'{self.value}'

    def leftmost(self):
        return self

    def rightmost(self):
        return self

    def explode(self):
        return False

    def split(self):
        if self.value < 10:
            return False
        half = self.value / 2.0
        self.parent[self.position()] = Pair(Literal(math.floor(half)), Literal(math.ceil(half)))
        return True

    def magnitude(self):
        return self.value

@dataclass
class Pair(SnailfishNumber):
    first: SnailfishNumber
    second: SnailfishNumber

    def __post_init__(self):
        self.first.parent = self
        self.second.parent = self

    def __repr__(self):
        return f'[{self.first}, {self.second}]'

    def __getitem__(self, idx) -> SnailfishNumber:
        if idx == 0: return 0
        if idx == 1: return 1
        raise IndexError

    def __setitem__(self, idx, value: SnailfishNumber):
        value.parent = self
        if idx == 0: self.first = value
        elif idx == 1: self.second = value
        else: raise IndexError

    def leftmost(self):
        return self.first.leftmost()

    def rightmost(self):
        return self.second.rightmost()

    def explode(self):
        if self.first.explode():
            return True
        if self.second.explode():
            return True

        try:
            if self.parent.parent.parent.parent is None:
                return False
        except AttributeError:
            return False

        if (left := self.first.left()) is not None:
            left.value += self.first.value
        if (right := self.second.right()) is not None:
            right.value += self.second.value
        self.parent[self.position()] = Literal(0)
        return True

    def split(self):
        if self.first.split():
            return True
        if self.second.split():
            return True
        return False

    def magnitude(self):
        return 3 * self.first.magnitude() + 2 * self.second.magnitude()


@aoc.register(__file__)
def answers():
    numbers = [SnailfishNumber.from_string(x)[0] for x in aoc.read_lines()]
    
    result: SnailfishNumber = sum(numbers)
    yield result.magnitude()

    mags = [(x+y).magnitude() for x,y in itertools.permutations(numbers, r=2)]
    yield max(mags)

if __name__ == '__main__':
    aoc.run()
