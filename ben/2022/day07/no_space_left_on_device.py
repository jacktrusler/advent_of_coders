from __future__ import annotations
import aoc
from collections import Counter
from dataclasses import dataclass, field
from functools import cached_property
from typing import Generator


@dataclass
class File:
    name: str
    size: int

@dataclass
class Directory:
    name: str = field(default='')
    parent: Directory = field(default=None, repr=False)
    contents: dict[str, File|Directory] = field(init=False, repr=False, default_factory=dict)

    def __getitem__(self, key: str) -> File | Directory:
        if key == '..': return self.parent
        if key == '/':  return self.top

        if key not in self.contents:
            self.contents = Directory(name=key, parent=self)
        return self.contents[key]

    @property
    def path(self) -> str:
        return '/' + '/'.join(reversed([x.name for x in self.parents()]))

    @cached_property
    def size(self) -> int:
        return sum(x.size for x in self.contents.values())

    @property
    def top(self) -> Directory:
        return list(self.parents())[-1]

    def parents(self) -> Generator[Directory]:
        level = self
        yield level
        while (level := level.parent) is not None:
            yield level

    def add_content(self, content: list[str]) -> Directory:
        for line in content:
            a, b = line.split()
            if a == 'dir' and b not in self.contents:
                self.contents[b] = Directory(name=b, parent=self)
            else:
                self.contents[b] = File(name=b, size=int(a))
        return self

    def size_report(self) -> Counter[str]:
        retval = Counter({self.path: self.size})
        for child in self.contents.values():
            if isinstance(child, Directory):
                retval |= child.size_report()
        return retval


def build_tree(commands: list[str]) -> Directory:
    cwd = Directory()
    for cmd in commands:
        if cmd.startswith('cd'):
            cwd = cwd[cmd.split()[-1]]
        elif cmd.startswith('ls'):
            cwd = cwd.add_content(cmd.splitlines()[1:])
    return cwd.top


@aoc.register(__file__)
def answers():
    commands = aoc.read_data().split('$ ')
    top_level = build_tree(commands)

    sizes = top_level.size_report()
    yield sum(x for x in sizes.values() if x <= 100_000)

    needed_space = 30_000_000 - (70_000_000 - sizes['/'])
    yield min(x for x in sizes.values() if x >= needed_space)

if __name__ == '__main__':
    aoc.run()
