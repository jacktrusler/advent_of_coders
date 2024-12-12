import aoc
import numpy as np
from numpy.typing import NDArray


def extrapolate(histories: NDArray[np.int_]) -> list[int]:
    _histories = np.copy(histories)
    ages = _histories[:,-1]

    while _histories.any():
        shifted = np.roll(_histories, -1, axis=1)
        _histories = (shifted - _histories)[:,:-1]
        ages += _histories[:,-1]
    return list(ages)


@aoc.register(__file__)
def answers():
    histories = np.array([x.split() for x in aoc.read_lines()], dtype=int)
    yield sum(extrapolate(histories))
    yield sum(extrapolate(np.flip(histories, axis=1)))

if __name__ == '__main__':
    aoc.run()
