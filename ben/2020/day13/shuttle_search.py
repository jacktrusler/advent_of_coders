from __future__ import annotations
import aoc
from dataclasses import dataclass
from functools import reduce
import math
import numpy as np
from operator import iand


def euclidean(a: int, b: int, c: int) -> int:
    gcd = math.gcd(a, b)
    k = int(c/gcd)
    q, r, s, t = [0,0], [a,b], [1,0], [0,1]
    
    while r[-1] != 0:
        quotient = r[-2] / r[-1]
        q.append(math.floor(quotient) if quotient >=0 else math.ceil(quotient))
        r.append(r[-2] - q[-1] * r[-1])
        s.append(s[-2] - q[-1] * s[-1])
        t.append(t[-2] - q[-1] * t[-1])

    s, t = s[-2], t[-2]
    if a*s + b*t == -gcd:
        k = -k
    return s*k

@dataclass
class Cycle:
    cycle_time: int
    offset: int

    def __init__(self, cycle_time: int, offset: int):
        self.cycle_time = cycle_time
        self.offset = offset % cycle_time

    def __and__(self, other: Cycle) -> Cycle:
        x = euclidean(self.cycle_time, -other.cycle_time, other.offset - self.offset)
        return Cycle(
            cycle_time=math.lcm(self.cycle_time, other.cycle_time),
            offset=int(self.cycle_time * x + self.offset)
        )


@aoc.register(__file__)
def answers():
    init_time, schedule = aoc.read_lines()

    bus_ids = np.array([int(x) for x in schedule.split(',') if x != 'x'])
    distances = bus_ids - (int(init_time) % bus_ids)
    idx = np.where(distances == min(distances))
    nearest_bus = bus_ids[idx][0]
    wait_time = distances[idx][0]
    yield nearest_bus * wait_time

    cycles = [Cycle(int(bus), -idx) for idx, bus in enumerate(schedule.split(',')) if bus != 'x']
    merged_cycle: Cycle = reduce(iand, cycles)
    yield merged_cycle.offset

if __name__ == '__main__':
    aoc.run()
