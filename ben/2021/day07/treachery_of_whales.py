import aoc
import numpy as np


def fuel_cost(dist):
    dist = np.where(dist > 0, dist+1, dist)
    return (dist * (dist-1)) / 2


@aoc.register(__file__)
def answers():
    crabs = np.array(list(map(int, aoc.read_data().split(','))))

    fuel = [np.abs(crabs-x).sum() for x in range(np.max(crabs)+1)]
    yield fuel[np.argmin(fuel)]

    fuel = [int(fuel_cost(crabs-x).sum()) for x in range(np.max(crabs)+1)]
    yield fuel[np.argmin(fuel)]

if __name__ == '__main__':
    aoc.run()
