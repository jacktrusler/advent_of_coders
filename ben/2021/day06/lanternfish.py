import aoc
from collections import Counter
import numpy as np


def reproduce(ages: dict[int,int], days: int) -> dict[int,int]:
    for _ in range(days):
        ages = {
            0: ages[1],
            1: ages[2],
            2: ages[3],
            3: ages[4],
            4: ages[5],
            5: ages[6],
            6: ages[7] + ages[0],
            7: ages[8],
            8: ages[0]
        }
    return ages


@aoc.register(__file__)
def answers():
    ages = Counter(np.array(list(map(int, aoc.read_data().split(',')))))

    ages = reproduce(ages, 80)
    yield sum(ages.values())

    ages = reproduce(ages, 256-80)
    yield sum(ages.values())

if __name__ == '__main__':
    aoc.run()
