import aoc
import itertools
import numpy as np
from numpy.typing import NDArray


def is_valid(window: NDArray, test_value: int) -> bool:
    for combo in itertools.combinations(window, 2):
        if sum(combo) == test_value:
            return True
    return False

def find_weakness(window: NDArray, target_value: int) -> NDArray:
    def weakness_range(sums: NDArray, start: int = 0) -> tuple[int, int]:
        try:
            idx = np.where(sums == target_value)[0][0]
            return start, start + idx + 1
        except IndexError:
            sums = sums - sums[0]
            return weakness_range(sums[1:], start+1)

    start, end = weakness_range(np.cumsum(window))
    return window[start:end]


@aoc.register(__file__)
def answers():
    PREAMBLE = 25
    data = np.array(list(map(int, aoc.read_lines())))

    idx = PREAMBLE
    while (is_valid(data[idx-PREAMBLE:idx], data[idx])):
        idx += 1
    yield idx

    weakness = find_weakness(data[:idx], data[idx])
    yield min(weakness) + max(weakness)

if __name__ == '__main__':
    aoc.run()
