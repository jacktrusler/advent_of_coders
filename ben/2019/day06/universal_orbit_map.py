import aoc
from collections import defaultdict
import functools
import heapq


ORBITS = defaultdict(set)
UNDIRECTIONAL_ORBITS = defaultdict(set)

@functools.cache
def count_orbits(object: str) -> int:
    _orbits = ORBITS[object]
    direct_orbits = len(_orbits)
    indirect_orbits = sum([count_orbits(x) for x in _orbits])
    return direct_orbits + indirect_orbits

def orbital_transfer(start: str, target: str) -> int:
    queue = [(0, start)]
    visited = set()
    distances = defaultdict(lambda: float('inf'))
    distances[start] = 0

    while queue:
        dist, planet = heapq.heappop(queue)
        if planet == target:
            return dist
        if planet in visited:
            continue

        visited.add(planet)
        neighbors = UNDIRECTIONAL_ORBITS[planet] - visited
        for neighbor in neighbors:
            _dist = dist + 1
            if _dist < distances[neighbor]:
                distances[neighbor] = _dist
                heapq.heappush(queue, (_dist, neighbor))

@aoc.register(__file__)
def answers():
    orbit_data = aoc.read_lines()
    for orbit in orbit_data:
        parent, child = orbit.split(')')
        ORBITS[child].add(parent)
        UNDIRECTIONAL_ORBITS[parent].add(child)
        UNDIRECTIONAL_ORBITS[child].add(parent)
    yield sum(map(count_orbits, list(ORBITS.keys())))

    start = next(iter(ORBITS['YOU']))
    target = next(iter(ORBITS['SAN']))
    yield orbital_transfer(start, target)

if __name__ == '__main__':
    aoc.run()
