from __future__ import annotations
from abc import ABC, abstractmethod
import aoc
from dataclasses import dataclass, field
from typing import ClassVar


class InfiniteLoopError(Exception):
    def __init__(self, acc):
        super().__init__('')
        self.accumulator = acc

@dataclass
class Instruction(ABC):
    op_str: ClassVar[str] = ''
    value: int

    def execute(self, state: Program) -> Program:
        self._execute(state)
        return state

    @abstractmethod
    def _execute(self, state: Program):
        pass

    @staticmethod
    def from_string(inst_str: str) -> Instruction:
        op, val = inst_str.split(' ')
        inst = [x for x in Instruction.__subclasses__() if x.op_str == op][0]
        return inst(int(val))
        
class Accumulate(Instruction):
    op_str: str = 'acc'

    def _execute(self, state):
        state.accumulator += self.value
        state.idx += 1

class Jump(Instruction):
    op_str: str = 'jmp'

    def _execute(self, state):
        state.idx += self.value

class NoOperation(Instruction):
    op_str: str = 'nop'

    def _execute(self, state):
        state.idx += 1

@dataclass
class Program:
    instructions: list[Instruction]
    accumulator: int = 0
    idx: int = 0
    _executed: set[int] = field(init=False, repr=False, default_factory=set)

    def execute(self) -> int:
        while True:
            if self.idx in self._executed:
                raise InfiniteLoopError(self.accumulator)
            self._executed.add(self.idx)

            try:
                self.instructions[self.idx].execute(self)
            except IndexError:
                return self.accumulator


@aoc.register(__file__)
def answers():
    instructions = [Instruction.from_string(x) for x in aoc.read_lines()]
    
    try:
        Program(instructions).execute()
    except InfiniteLoopError as e:
        yield e.accumulator

    for idx, inst in enumerate(instructions):
        og = inst.__class__
        if og == Accumulate: continue
        elif og == Jump: instructions[idx] = NoOperation(inst.value)
        elif og == NoOperation: instructions[idx] = Jump(inst.value)

        try:
            accumulator = Program(instructions).execute()
            break
        except InfiniteLoopError as e:
            instructions[idx] = og(inst.value)
    yield accumulator

if __name__ == '__main__':
    aoc.run()
