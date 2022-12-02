from __future__ import annotations
import aoc
import collections
import re
from typing import Counter


class BagDict(dict):
    def __missing__(self, key):
        self[key] = Bag(key)
        return self[key]

class Bag:
    def __init__(self, color: str):
        self.color: str = color
        self.parents: set[Bag] = set()
        self.children: Counter[Bag] = collections.Counter({})

    def __repr__(self):
        return f'Bag({self.color})'

    def __hash__(self):
        return hash(self.color)

    def add_child(self, child: Bag, amount: int):
        self.children[child] = amount
        child.parents.add(self)

    def all_parents(self) -> set[Bag]:
        ancestors = [x.all_parents() for x in self.parents]
        return self.parents.union(*ancestors)

    def all_children(self, amount: int = 1) -> Counter[Bag]:
        children = Counter({bag: num*amount for bag, num in self.children.items()})
        children = sum([child.all_children(num) for child, num in children.items()], start=children)
        return children

    @staticmethod
    def from_string(data: str, tree: BagDict):
        color = re.match(r'(.*) bags contain', data)[1]
        children = re.findall(r'(\d+?) (.+?) bags?', data)

        bag = tree[color]
        [bag.add_child(tree[child], int(amount)) for amount, child in children]


@aoc.register(__file__)
def answers():
    bags = BagDict()
    [Bag.from_string(line, bags) for line in aoc.read_lines()]

    shiny_gold_parents = bags['shiny gold'].all_parents()
    yield len(shiny_gold_parents)

    shiny_gold_children = bags['shiny gold'].all_children()
    yield sum(shiny_gold_children.values())

if __name__ == '__main__':
    aoc.run()
