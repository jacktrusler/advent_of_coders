from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable


IntcodeProgram = Iterable[int]

class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1

class Operation(ABC):
    opcode: int = None
    length: int = 0

    def __init__(self, vm: IntcodeVM):
        self.vm = vm
        self.pc = vm.pc + self.length

        chunk = vm.program[vm.pc : vm.pc + self.length]
        instruction = str(chunk[0]).zfill(5)
        self.modes = tuple(map(int, reversed(instruction[:3])))
        self.args = tuple(vm.program[vm.pc + i] for i in range(1, self.length))

    def decode_arg(self, i: int) -> int:
        value = self.args[i]
        match ParameterMode(self.modes[i]):
            case ParameterMode.POSITION: return self.vm.program[value]
            case ParameterMode.IMMEDIATE: return value
            case _: raise Exception("Invalid mode detected")

    @abstractmethod
    def exec(self, inputs: Iterable[int]) -> int:
        raise NotImplementedError

    @staticmethod
    def create(vm: IntcodeVM) -> Operation:
        instruction = str(vm.program[vm.pc]).zfill(5)
        opcode = int(instruction[3:])
        try:    
            return next(x for x in Operation.__subclasses__() if x.opcode == opcode)(vm)
        except StopIteration:
            raise Exception(f'No opcode detected matching {opcode}')
    
class OpAdd(Operation):
    opcode = 1
    length = 4

    def exec(self, inputs: Iterable[int]) -> int:
        self.vm[self.args[2]] = self.decode_arg(0) + self.decode_arg(1)

class OpMultiply(Operation):
    opcode = 2
    length = 4

    def exec(self, inputs: Iterable[int]) -> int:
        self.vm[self.args[2]] = self.decode_arg(0) * self.decode_arg(1)

class OpInput(Operation):
    opcode = 3
    length = 2

    def exec(self, inputs: Iterable[int]) -> int:
        self.vm[self.args[0]] = next(inputs)
    
class OpOutput(Operation):
    opcode = 4
    length = 2

    def exec(self, inputs: Iterable[int]) -> int:
        return self.decode_arg(0)
    
class OpJumpIfTrue(Operation):
    opcode = 5
    length = 3

    def exec(self, inputs: Iterable[int]) -> int:
        self.pc = self.decode_arg(1) if self.decode_arg(0) else self.pc
    
class OpJumpIfFalse(Operation):
    opcode = 6
    length = 3

    def exec(self, inputs: Iterable[int]) -> int:
        self.pc = self.decode_arg(1) if not self.decode_arg(0) else self.pc
    
class OpLessThan(Operation):
    opcode = 7
    length = 4

    def exec(self, inputs: Iterable[int]) -> int:
        self.vm[self.args[2]] = 1 if self.decode_arg(0) < self.decode_arg(1) else 0

class OpEquals(Operation):
    opcode = 8
    length = 4

    def exec(self, inputs: Iterable[int]) -> int:
        self.vm[self.args[2]] = 1 if self.decode_arg(0) == self.decode_arg(1) else 0

class OpHalt(Operation):
    opcode = 99
    length = 1

    def exec(self, inputs: Iterable[int]) -> int:
        self.vm.running = False
        return self.vm.last_output
    

class IntcodeVM:
    def __init__(self, program: list[int]):
        self.__original = program
        self.program = self.__original[:]
        self.running = True
        self.pc = 0
        self.last_output = None

    def __getitem__(self, idx):
        return self.program[idx]
    
    def __setitem__(self, idx, val):
        self.program[idx] = val

    def run(self, *args) -> int:
        inputs = iter(args)

        while self.running:
            op = Operation.create(self)
            out = op.exec(inputs)
            self.pc = op.pc
            if out is not None:
                self.last_output = out
                return out
        return self.last_output

    def reset(self):
        self.running = True
        self.pc = 0
        self.program = self.__original[:]