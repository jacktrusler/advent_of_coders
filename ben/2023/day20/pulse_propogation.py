from __future__ import annotations
import abc
import aoc
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
import itertools
import re
from typing import ClassVar, Generator

# class Pulse(Enum):
#     LOW = 0
#     HIGH = 1

class GetItemMeta(type):
    def __getitem__(cls, key):
        return cls._registry[key]
    
    def __iter__(cls):
        return iter(cls._registry.values())
ModuleMeta = type('ModuleMeta', (abc.ABCMeta, GetItemMeta), {})

@dataclass
class Module(abc.ABC, metaclass=ModuleMeta):
    _INDICATOR: ClassVar[str] = None
    id: str
    outputs: list[Module] = field(default_factory=list, repr=False)
    lows: int = field(default=0, repr=False)
    highs: int = field(default=0, repr=False)
    state: bool = False

    def __post_init__(self):
        if not hasattr(Module, '_registry'):
            Module._registry = {}
        Module._registry[self.id] = self

    @classmethod
    def from_string(cls, input: str) -> Module:
        id, outputs = input.split('->')
        for module in cls.__subclasses__():
            if (m := re.match(module._INDICATOR, id.strip())):
                id = m.group(1)
                break
        outputs = outputs.strip().split(', ')
        return module(id, outputs)

    def emit(self) -> Generator[tuple[Module, bool]]:
        if self.state:
            self.highs += len(self.outputs)
        else:
            self.lows += len(self.outputs)
        return ((target, self.state) for target in self.outputs)

    @abc.abstractmethod
    def receive(self, pulse: bool, **kwargs) -> Generator[tuple[Module, bool]]:
        pass
    

class FlipFlop(Module):
    _INDICATOR: ClassVar[str] = r'%(.*)'

    def receive(self, pulse: bool, **kwargs):
        if not pulse:
            self.state = not self.state
            yield from self.emit()

class Conjunction(Module):
    _INDICATOR: ClassVar[str] = r'&(.*)'

    @property
    def memory(self) -> dict[str, bool]:
        if hasattr(self, '_cache'):
            return self._cache
        self._cache = {m.id: False for m in Module if self.id in m.outputs}
        return self._cache

    def receive(self, pulse: bool, sender: str, **kwargs):
        self.memory[sender] = pulse
        self.state = not all(self.memory.values())
        yield from self.emit()

class Broadcaster(Module):
    _INDICATOR: ClassVar[str] = r'(broadcaster)'

    def receive(self, pulse: bool, **kwargs):
        self.state = pulse
        yield from self.emit()

def push_button(modules: dict[str, Module], catch: tuple[str, bool] = False):
    queue: deque[tuple[Module, bool, str]] = deque([('broadcaster', False, None)])
    while queue:
        module_id, pulse, sender = queue.popleft()
        if catch and (module_id, pulse) == catch:
            raise IndexError
        try:
            module = modules[module_id]
        except KeyError:
            continue
        for id, p in module.receive(pulse, sender=sender):
            queue.append((id, p, module.id))



@aoc.register(__file__)
def answers():
    modules = {x.id: x for x in map(Module.from_string, aoc.read_lines())}

    for n in itertools.count(start=1):
        try:
            push_button(modules, catch=('rx', False))
        except IndexError:
            break
        if n == 1000:
            all_lows = sum(x.lows for x in modules.values()) + n
            all_highs = sum(x.highs for x in modules.values())
            yield all_lows * all_highs
            break
        if n % 10000 == 0:
            print(n)

    
    

if __name__ == '__main__':
    aoc.run()
