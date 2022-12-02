from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
import aoc
from collections import deque
from dataclasses import dataclass, field
from functools import reduce
from typing import ClassVar


class PacketParseError(Exception):
    pass

@dataclass
class Packet(ABC):
    version: int
    length: int = field(default=0, repr=False)
    type_id: ClassVar[int] = -1
    TYPE_DICT: ClassVar[dict] = {}

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if (type_id := cls.type_id) >= 0:
            Packet.TYPE_DICT[type_id] = cls

    @abstractproperty
    def value(self):
        pass

    def _read(self, transmission: deque[str], size: int, as_int=True) -> str:
        try:
            contents = ''.join([transmission.popleft() for _ in range(size)])
        except IndexError:
            raise PacketParseError
        self.length += size
        return int(contents, 2) if as_int == True else contents

    def version_total(self) -> int:
        return self.version

    @staticmethod
    def parse(transmission: deque[str]) -> Packet:
        if len(transmission) < 6:
            raise PacketParseError

        opening = ''.join([transmission.popleft() for _ in range(6)])
        version = int(opening[:3], 2)
        packet_type = int(opening[3:6], 2)

        packet_class = Packet.TYPE_DICT[packet_type]
        packet = packet_class(version=version, length=6)._parse(transmission)
        # Do remainder
        return packet

    @abstractmethod
    def _parse(self, transmission: list[str]) -> Packet:
        pass
        

@dataclass
class LiteralPacket(Packet):
    type_id = 4
    stored_value: int = field(default=0)

    @property
    def value(self):
        return self.stored_value

    def _parse(self, transmission) -> Packet:
        value_strings = []
        leading_bit = True
        while leading_bit:
            try:
                leading_bit = bool(self._read(transmission, 1))
                value_strings.append(self._read(transmission, 4, as_int=False))
            except (IndexError, ValueError):
                raise PacketParseError

        self.stored_value = int(''.join(value_strings), 2)
        return self

@dataclass
class OperatorPacket(Packet, ABC):
    packets: list[Packet] = field(default_factory=list)

    def version_total(self):
        return sum([x.version_total() for x in self.packets]) + self.version

    def read_packet(self, transmission: list[str]) -> Packet:
        packet = Packet.parse(transmission)
        self.packets.append(packet)
        self.length += packet.length
        return packet.length

    def _parse(self, transmission):
        lenTypeID = self._read(transmission, 1)
        match(lenTypeID):
            case 0:
                subLength = self._read(transmission, 15)
                bits = 0
                while bits < subLength:
                    bits += self.read_packet(transmission)
            case 1:
                numPackets = self._read(transmission, 11)
                for _ in range(numPackets):
                    self.read_packet(transmission)
            case _:
                raise PacketParseError()
        return self


class SumPacket(OperatorPacket):
    type_id = 0
    
    @property
    def value(self):
        return sum([x.value for x in self.packets])

class ProductPacket(OperatorPacket):
    type_id = 1

    @property
    def value(self):
        return reduce(lambda x, y: x*y, [x.value for x in self.packets])

class MinimumPacket(OperatorPacket):
    type_id = 2

    @property
    def value(self):
        return min([x.value for x in self.packets])

class MaximumPacket(OperatorPacket):
    type_id = 3

    @property
    def value(self):
        return max([x.value for x in self.packets])

class GreaterThanPacket(OperatorPacket):
    type_id = 5

    @property
    def value(self):
        return self.packets[0].value > self.packets[1].value

class LessThanPacket(OperatorPacket):
    type_id = 6

    @property
    def value(self):
        return self.packets[0].value < self.packets[1].value

class EqualToPacket(OperatorPacket):
    type_id = 7
    
    @property
    def value(self):
        return self.packets[0].value == self.packets[1].value


@aoc.register(__file__)
def answers():
    transmission = deque(bin(int('F' + aoc.read_data(), 16))[6:])

    packets = []
    while transmission:
        try:
            packets.append(Packet.parse(transmission))
        except PacketParseError:
            break

    yield sum([x.version_total() for x in packets])
    yield sum([x.value for x in packets])

if __name__ == '__main__':
    aoc.run()
