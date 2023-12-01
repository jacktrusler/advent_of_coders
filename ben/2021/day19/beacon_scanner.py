from __future__ import annotations
import aoc
from collections import deque
from enum import Enum, auto
import itertools
import numpy as np
from numpy.typing import NDArray
import re


Location = tuple[int, int, int]

class Orientation(Enum):
    """ 
    Enum for the orientation of a scanner. P for positive, N for negative, in order forward, up, right.
    For example, NXPYNZ means forward is -X, up is +Y, and right is -Z
    """
    PYPZPX = auto(); PYNZNX = auto(); PYPXNZ = auto(); PYNXPZ = auto()
    NYPZNX = auto(); NYNZPX = auto(); NYPXPZ = auto(); NYNXNZ = auto()
    PXPZNY = auto(); PXNZPY = auto(); PXPYPZ = auto(); PXNYNZ = auto()
    NXPZPY = auto(); NXNZNY = auto(); NXPYNZ = auto(); NXNYPZ = auto()
    PZPXPY = auto(); PZNXNY = auto(); PZPYNX = auto(); PZNYPX = auto()
    NZPXNY = auto(); NZNXPY = auto(); NZPYPX = auto(); NZNYNX = auto()

def distance(x: Location, y: Location) -> float:
    return np.linalg.norm(np.asarray(x) - np.asarray(y), axis=1)

def trilateration(p1: Location, p2: Location, p3: Location, r1: int, r2: int, r3: int) -> tuple[Location, Location]:
    """
    Determine the points where three spheres (defined by point and radius) intersect
    https://gis.stackexchange.com/questions/66/trilateration-using-3-latitude-longitude-points-and-3-distances/415 
    """
    _p1 = np.array([0, 0, 0])
    _p2 = np.array([p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]])
    _p3 = np.array([p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]])
    v1 = _p2 - _p1
    v2 = _p3 - _p1

    ex = v1/np.linalg.norm(v1)
    i = np.dot(ex, v2)
    ey = (v2 - i*ex)/np.linalg.norm(v2 - i*ex)
    ez = np.cross(ex, ey)
    d = np.linalg.norm(v1)
    j = np.dot(ey, v2)

    x = (np.square(r1) - np.square(r2) + np.square(d))/(2*d)
    y = ((np.square(r1) - np.square(r3) + np.square(i) + np.square(j))/(2*j)) - ((i/j)*x)
    z1 = np.sqrt(np.square(r1) - np.square(x) - np.square(y))
    z2 = -z1

    result1 = p1 + x*ex + y*ey + z1*ez
    result2 = p1 + x*ex + y*ey + z2*ez
    return tuple(np.rint(result1).astype(int)), tuple(np.rint(result2).astype(int))

def manhattan_distance(p1: Location, p2: Location) -> int:
    """ Calculate the Manhattan distance between two points in 3D space """
    return sum([
        abs(p2[0] - p1[0]),
        abs(p2[1] - p1[1]),
        abs(p2[2] - p1[2])
    ])


class Scanner:
    def __init__(self, id: int, beacons: NDArray):
        self.id = id
        self._beacon_data = beacons
        self.orientation: Orientation = Orientation.PXPYPZ
        self.location: Location = None

    def beacons(self) -> set[Location]:
        orien_str = self.orientation.name
        forward, upward, right = orien_str[:2], orien_str[2:4], orien_str[4:]

        letter_map = { 'X': 0, 'Y': 1, 'Z': 2, 'P': 1, 'N': -1 }
        beacon_data = np.full_like(self._beacon_data, 0, dtype=int)
        beacon_data[:, letter_map[right[1]]] = letter_map[right[0]] * self._beacon_data[:, 0]
        beacon_data[:, letter_map[forward[1]]] = letter_map[forward[0]] * self._beacon_data[:, 1]
        beacon_data[:, letter_map[upward[1]]] = letter_map[upward[0]] * self._beacon_data[:, 2]
        
        start = self.location if self.location is not None else (0, 0, 0)
        return set(tuple(x) for x in (beacon_data + start))

    def matching_beacons(self, other: Scanner) -> list[tuple[Location, Location]]:
        my_beacons, other_beacons = self.beacons(), other.beacons()
        my_dists = {beacon: set(distance(beacon, np.asarray(list(my_beacons)))) for beacon in my_beacons}
        other_dists = {beacon: set(distance(beacon, np.asarray(list(other_beacons)))) for beacon in other_beacons}
        return [(x[0], y[0]) for x, y in itertools.product(my_dists.items(), other_dists.items()) 
                      if len(x[1] & y[1]) >= 12]

    def _determine_orientation(self, beacons_to_match: list[Location]) -> bool:
        """ Use trial and error to determine the correct orientation of the scanner """
        beacons_to_match = {tuple(x) for x in beacons_to_match}
        for o in Orientation:
            self.orientation = o
            if beacons_to_match <= self.beacons():
                return True
        return False

    def place_relative_to(self, other: Scanner) -> bool:
        # Need at least 12 matching beacons to place
        matches = self.matching_beacons(other)
        if len(matches) < 12:
            return False

        # Trilaterate to find the starting point of the scanner. Each result will get 2 points. Find the common one.
        beacons = [x[1] for x in matches]
        radii = distance([x[0] for x in matches], (0,0,0))
        t1 = set(trilateration(beacons[0], beacons[1], beacons[2], radii[0], radii[1], radii[2]))
        t2 = set(trilateration(beacons[3], beacons[4], beacons[5], radii[3], radii[4], radii[5]))
        (point,) = t1 & t2
        self.location = point

        # Determine the orientation of the scanner
        if not self._determine_orientation(beacons):
            return False
        return True

    @staticmethod
    def from_string(_str: str) -> Scanner:
        lines = _str.splitlines()
        scanner_id = int(re.match(r'--- scanner (\d+) ---', lines[0]).group(1))
        beacons = np.array([list(map(int, x.split(','))) for x in lines[1:]])
        return Scanner(scanner_id, beacons)


@aoc.register(__file__)
def answers():
    scanners = [Scanner.from_string(x) for x in aoc.read_chunks()]
    scanners[0].location = (0,0,0)
    
    # Attempt to place the scanners until there are none left to place
    placed, unplaced = deque(scanners[:1]), set(scanners[1:])
    while placed:
        placed_scanner = placed.pop()
        newly_placed = {scanner for scanner in unplaced if scanner.place_relative_to(placed_scanner)}
        placed.extend(newly_placed)
        unplaced = unplaced ^ newly_placed
    if unplaced:
        raise Exception(f'Couldnt place scanners: {unplaced}')

    # Gather all of the beacons and report the number of unique ones
    all_beacons = set()
    for x in scanners:
        all_beacons = all_beacons | set([tuple(y) for y in x.beacons()])
    yield len(all_beacons)

    # Calculate the manhattan distances of each scanner to one another and report the max
    yield max([manhattan_distance(x.location, y.location) for x, y in itertools.combinations(scanners, 2)])

if __name__ == '__main__':
    aoc.run()
