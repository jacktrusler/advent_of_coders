from __future__ import annotations
from collections import deque
from enum import Enum, auto
from itertools import combinations
import numpy as np
from numpy.typing import NDArray
from typing import Tuple, List, Dict

# Typehint defs
Point = Tuple[int, int, int]


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


def distance(p1:Point|NDArray, p2:Point|NDArray) -> float|NDArray:
    """ Calculate the distance between two points in 3D space """
    try:
        x1, y1, z1 = p1[:,0], p1[:,1], p1[:,2]
    except (IndexError, TypeError):
        x1, y1, z1 = p1
    try:
        x2, y2, z2 = p2[:,0], p2[:,1], p2[:,2]
    except (IndexError, TypeError):
        x2, y2, z2 = p2
    return np.sqrt(np.square(x2-x1) + np.square(y2-y1) + np.square(z2-z1))


def trilateration(p1:Point, p2:Point, p3:Point, r1:int, r2:int, r3:int) -> Tuple[Point, Point]:
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


def manhattan_distance(p1:Point, p2:Point) -> int:
    """ Calculate the Manhattan distance between two points in 3D space """
    return sum([
        abs(p2[0] - p1[0]),
        abs(p2[1] - p1[1]),
        abs(p2[2] - p1[2])
    ])


class Scanner:
    """ Represents a scanner and all of its beacons (using the knowledge it has) """
    def __init__(self, scanner_data):
        self.id:int = scanner_data[0].replace('-', '').strip().split(' ')[1]
        self.location:Point = None
        self.orientation:Orientation = Orientation.PYPZPX
        self._beacon_data:NDArray = np.array([x.split(',') for x in scanner_data[1:] if x], dtype=int)

    def __repr__(self):
        return f'Scanner({self.id})'

    @property
    def beacons(self) -> List[Point]:
        """ Obtain the beacon points using the location, orientation, and raw beacon data """
        orien_str = self.orientation.name
        forward, upward, right = orien_str[:2], orien_str[2:4], orien_str[4:]

        letter_map = { 'X': 0, 'Y': 1, 'Z': 2, 'P': 1, 'N': -1 }
        beacon_data = np.full_like(self._beacon_data, 0, dtype=int)

        beacon_data[:, letter_map[right[1]]] = letter_map[right[0]] * self._beacon_data[:, 0]
        beacon_data[:, letter_map[forward[1]]] = letter_map[forward[0]] * self._beacon_data[:, 1]
        beacon_data[:, letter_map[upward[1]]] = letter_map[upward[0]] * self._beacon_data[:, 2]

        start = self.location if self.location is not None else (0, 0, 0)
        beacon_data = beacon_data + start
        return [tuple(b) for b in beacon_data]

    def _matching_beacons(self, other:Scanner) -> Dict[Point, Point]:
        """ Obtain the beacons that are matched with the given scanner """
        my_beacons, other_beacons = self.beacons, other.beacons
        dist_dict = {beacon: distance(beacon, np.array(my_beacons)) for beacon in my_beacons}

        # Try to match based on distance to other known beacons
        matching_beacons = {}
        for other_beacon in other_beacons:
            other_dists = distance(other_beacon, np.array(other_beacons))
            
            for my_beacon, my_dists in dist_dict.items():
                matches = set(my_dists) & set(other_dists)

                # 12 or more makes a match
                if len(matches) >= 12:
                    matching_beacons[other_beacon] = my_beacon
                    break
            if other_beacon in matching_beacons:
                dist_dict.pop(my_beacon)

        return matching_beacons

    def _determine_orientation(self, beacons_to_match: List[Point]) -> bool:
        """ Use trial and error to determine the correct orientation of the scanner """
        for o in Orientation:
            self.orientation = o
            beacons = self.beacons
            if all([beacon in beacons for beacon in beacons_to_match]):
                return True
        return False

    def place_using(self, other:Scanner) -> bool:
        """ Attempt to set the scanner's location and orientation using data from another scanner """
        # Match each beacon's distance to all other beacons of that scanner for both scanners
        # Need at least 12 matching beacons to place
        matches = self._matching_beacons(other)
        if len(matches) < 12:
            return False

        # Trilaterate to find the starting point of the scanner. Each result will get 2 points. Find the common one.
        beacons = list(matches.keys())
        radii = distance(np.array(list(matches.values())), (0,0,0))
        t1 = set(trilateration(beacons[0], beacons[1], beacons[2], radii[0], radii[1], radii[2]))
        t2 = set(trilateration(beacons[3], beacons[4], beacons[5], radii[3], radii[4], radii[5]))
        (point,) = t1 & t2
        self.location = point

        # Determine the orientation of the scanner
        if not self._determine_orientation(beacons):
            return False
        return True


# Read in the input data and translate it to Scanner objects
with open('2021/day19/scanner_report.txt') as f:
    scanner_report = f.read().split('\n---')
    scanner_report = [x.split('\n') for x in scanner_report]
scanners = [Scanner(x) for x in scanner_report]
scanners[0].location = (0, 0, 0)

# Attempt to place the scanners until there are none left to place
placed, unplaced = deque(scanners[:1]), set(scanners[1:])
while placed:
    placed_scanner = placed.pop()
    newly_placed = {scanner for scanner in unplaced if scanner.place_using(placed_scanner)}
    placed.extend(newly_placed)
    unplaced = unplaced ^ newly_placed
if unplaced:
    raise Exception(f'Couldnt place scanners: {unplaced}')

# Gather all of the beacons and report the number of unique ones
all_beacons = set()
for x in scanners:
    all_beacons = all_beacons | set(x.beacons)
print(len(all_beacons))

# Calculate the manhattan distances of each scanner to one another and report the max
manhattans = [manhattan_distance(x.location, y.location) for x, y in combinations(scanners, 2)]
print(max(manhattans))