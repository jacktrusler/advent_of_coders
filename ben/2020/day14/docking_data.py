from abc import ABC, abstractmethod
import aoc
import numpy as np
import re
        

class Program(ABC):
    def __init__(self):
        self.mask: str = ''
        self.memory: dict[int, int] = {}

    def execute(self, cmd_list: list[str]) -> int:
        for cmd in cmd_list:
            try:
                mem_data = re.match(r'mem\[(?P<address>.*)\] = (?P<value>.*)', cmd).groupdict()
                self.memory.update(self._write_memory(int(mem_data['address']), int(mem_data['value'])))
                continue
            except AttributeError:
                pass

            self.mask = re.match(r'mask = (?P<value>.*)', cmd).group(1)

        return sum(self.memory.values())

    @abstractmethod
    def _write_memory(self, address: int, value: int) -> dict[int, int]:
        pass

class ProgramV1(Program):
    def _write_memory(self, address, value):
        retval = value
        for idx, bit in enumerate(reversed(self.mask)):
            try:
                retval = retval | (2 ** idx) if int(bit) else retval & ~(2 ** idx)
            except ValueError:
                continue
        return {address: retval}

class ProgramV2(Program):
    def _write_memory(self, address, value):
        address_str = bin(address)[2:].zfill(36)
        mask_bits = np.array(list(self.mask))
        adr_bits = np.array(list(address_str))

        adr_bits = np.where(np.logical_or(adr_bits == 'X', mask_bits == 'X'), 'X', adr_bits)
        adr_bits = np.where(np.logical_and(adr_bits != 'X', mask_bits == '1'), '1', adr_bits)

        addresses = np.array([0], dtype=np.longlong)
        for idx, val in enumerate(reversed(adr_bits)):
            if val == 'X':
                addresses = np.concatenate((addresses, addresses + 2 ** idx))
            else:
                addresses += (2 ** idx) * int(val)
        return {x: value for x in addresses}


@aoc.register(__file__)
def answers():
    commands = aoc.read_lines()
    yield ProgramV1().execute(commands)
    yield ProgramV2().execute(commands)

if __name__ == '__main__':
    aoc.run()
