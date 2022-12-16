from __future__ import annotations
import aoc
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from math import prod
from operator import add, mul
import re
from typing import Callable, ClassVar, Generator


@dataclass
class Monkey:
    id: int
    test: int = field(repr=False)
    items: deque[int] = field(default_factory=deque)
    num_inspects: int = field(init=False, default=0, repr=False)
    _inspect: Callable[[int], int] = field(init=False, default_factory=lambda: None, repr=False)
    _throw_target: Callable[[bool], int] = field(init=False, default_factory=lambda: None, repr=False)
    _MODULO: ClassVar[int] = 1

    def __post_init__(self):
        Monkey._MODULO *= self.test

    def turns(self, relief: int) -> Generator[tuple[int,int]]:
        while self.items:
            self.num_inspects += 1
            item = self.items.popleft()
            item = (self._inspect(item) // relief) % Monkey._MODULO
            target = self._throw_target(item % self.test == 0)
            yield item, target        

    @staticmethod
    def from_string(monkey_data: str) -> Monkey:
        regex =  r'Monkey (\d+):\n'
        regex += r'  Starting items: (.*)\n'
        regex += r'  Operation: new = (.*) (\*|\+) (.*)\n'
        regex += r'  Test: divisible by (\d+)\n'
        regex += r'    If true: throw to monkey (\d+)\n'
        regex += r'    If false: throw to monkey (\d+)'
        m = re.match(regex, monkey_data).groups()
        
        monkey_id, test_val = int(m[0]), int(m[5])
        left, op, right = m[2], mul if m[3] == '*' else add, m[4]
        true_throw, false_throw = int(m[6]), int(m[7])
        items = deque([int(x.strip()) for x in m[1].split(',')])

        retval = Monkey(id=monkey_id, test=test_val, items=items)
        retval._inspect = lambda x: op(x if left == 'old' else int(left), x if right == 'old' else int(right))
        retval._throw_target = lambda x: true_throw if x else false_throw
        return retval


def perform_round(monkeys: list[Monkey], relief: int) -> list[Monkey]:
    for monkey in monkeys:
        for item, target in monkey.turns(relief=relief):
            monkeys[target].items.append(item)
    return monkeys

@aoc.register(__file__)
def answers():
    monkeys = [Monkey.from_string(x) for x in aoc.read_chunks()]

    monkeys1 = deepcopy(monkeys)
    for _ in range(20):
        monkeys1 = perform_round(monkeys1, relief=3)
    monkey_business = sorted([x.num_inspects for x in monkeys1])[-2:]
    yield prod(monkey_business)

    monkeys2 = deepcopy(monkeys)
    for _ in range(10000):
        monkeys2 = perform_round(monkeys2, relief=1)
    monkey_business = sorted([x.num_inspects for x in monkeys2])[-2:]
    yield prod(monkey_business)

if __name__ == '__main__':
    aoc.run()
