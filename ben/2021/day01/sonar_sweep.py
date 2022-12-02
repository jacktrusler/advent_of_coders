import aoc
import numpy as np


@aoc.register(__file__)
def answers():
    data = np.array(list(map(int, aoc.read_lines())))

    diff = data[1:] - data[:-1]
    yield np.count_nonzero(diff > 0)

    windows = data[:-2] + data[1:-1] + data[2:]
    diff = windows[1:] - windows[:-1]
    yield np.count_nonzero(diff > 0)

if __name__ == '__main__':
    aoc.run()
