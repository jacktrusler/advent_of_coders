from __future__ import annotations
import aoc
import numpy as np
from numpy.typing import NDArray
import re


class Scanner:
    def __init__(self, id: int, beacons: NDArray):
        self.id = id
        self.beacons = beacons

    @staticmethod
    def from_string(_str: str) -> Scanner:
        lines = _str.splitlines()
        scanner_id = int(re.match(r'--- scanner (\d+) ---', lines[0]).group(1))
        beacons = np.array([list(map(int, x.split(','))) for x in lines[1:]])
        return Scanner(scanner_id, beacons)


@aoc.register(__file__)
def answers():
    scanners = [Scanner.from_string(x) for x in aoc.read_chunks()]

if __name__ == '__main__':
    aoc.run()
