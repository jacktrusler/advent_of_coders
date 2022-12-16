from __future__ import annotations
from enum import Enum, auto
import aoc
import json
from math import prod


class CompareResult(Enum):
    LT = auto()
    EQ = auto()
    GT = auto()

class Packet:
    def __init__(self, content: str):
        self._data = json.loads(content)

    def __lt__(self, other: Packet):
        return Packet.compare(self._data, other._data) == CompareResult.LT

    @staticmethod
    def compare(val_a: list[int] | int, val_b: list[int] | int) -> CompareResult:
        isint_a, isint_b = isinstance(val_a, int), isinstance(val_b, int)
        if isint_a and isint_b:
            if val_a < val_b: return CompareResult.LT
            if val_a > val_b: return CompareResult.GT
            return CompareResult.EQ

        list_a = [val_a] if isint_a else val_a
        list_b = [val_b] if isint_b else val_b
        for x, y in zip(list_a, list_b):
            if (result := Packet.compare(x, y)) != CompareResult.EQ:
                return result

        if len(list_a) < len(list_b): return CompareResult.LT
        if len(list_a) > len(list_b): return CompareResult.GT
        return CompareResult.EQ


@aoc.register(__file__)
def answers():
    pairs = [tuple(Packet(line) for line in chunk.splitlines())
             for chunk in aoc.read_chunks()]

    right_order = [i for i, pair in enumerate(pairs, start=1) if pair[0] < pair[1]]
    yield sum(right_order)

    decoder_packets = [Packet('[[2]]'), Packet('[[6]]')]
    all_packets = sorted([packet for pair in pairs for packet in pair] + decoder_packets)
    decoder_indices = [all_packets.index(p) + 1 for p in decoder_packets]
    yield prod(decoder_indices)

if __name__ == '__main__':
    aoc.run()
