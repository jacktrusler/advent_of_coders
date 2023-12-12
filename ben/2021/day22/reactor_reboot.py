from __future__ import annotations
import aoc
from aoc.utils import Interval
from dataclasses import dataclass, replace
from functools import cached_property
import re
    

@dataclass(frozen=True)
class Zone:
    x: Interval
    y: Interval
    z: Interval
    active: bool = True

    def __and__(self, other: Zone) -> Zone:
        if not (x := self.x & other.x) or not (y := self.y & other.y) or not (z := self.z & other.z):
            return None
        return Zone(x, y, z, self.active)
    
    def __sub__(self, other: Zone) -> Zone:
        if not (z := self & other):
            return None
        return replace(z, active=not other.active)
        
    @cached_property
    def volume(self) -> int:
        if not self:
            return 0
        vol = (len(self.x)) * (len(self.y)) * (len(self.z))
        return vol if self.active else -vol
    
    def __bool__(self) -> bool:
        return not self.empty
    
    @cached_property
    def empty(self):
        return self.x == None or self.y == None or self.z == None
    
    @staticmethod
    def from_string(line: str) -> Zone:
        m = re.match(r'(?P<state>on|off) x=(?P<min_x>-?\d+)..(?P<max_x>-?\d+),y=(?P<min_y>-?\d+)..(?P<max_y>-?\d+),z=(?P<min_z>-?\d+)..(?P<max_z>-?\d+)', line).groupdict()
        return Zone(
            active = m['state'] == 'on',
            x = Interval(int(m['min_x']), int(m['max_x'])),
            y = Interval(int(m['min_y']), int(m['max_y'])),
            z = Interval(int(m['min_z']), int(m['max_z']))
        )

def process_instructions(zones: list[Zone], valid_zone: Zone = None) -> int:
    applied_zones: list[Zone] = []
    for zone in zones:
        if valid_zone:
            zone = zone & valid_zone
        if not zone:
            continue

        intersections = ((zone - z) for z in applied_zones)
        applied_zones += [x for x in intersections if x]
        if zone.active:
            applied_zones.append(zone)
    return sum(z.volume for z in applied_zones)


@aoc.register(__file__)
def answers():
    zones = [Zone.from_string(x) for x in aoc.read_lines()]

    reboot_interval = Interval(-50, 50)
    reboot_zone = Zone(x=reboot_interval, y=reboot_interval, z=reboot_interval)
    yield(process_instructions(zones, valid_zone=reboot_zone))
    yield(process_instructions(zones))


if __name__ == '__main__':
    aoc.run()
