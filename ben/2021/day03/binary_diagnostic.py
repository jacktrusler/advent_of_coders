import aoc
import numpy as np
from numpy.typing import NDArray



def most_common(data: NDArray) -> int:
    return 1 if np.count_nonzero(data) >= len(data) / 2 else 0

def bits_to_int(data: NDArray) -> int:
    return data.dot(1 << np.arange(data.shape[-1] - 1, -1, -1))

def reduce_data(data: NDArray, common=True) -> int:
    retval = data.copy()
    for i in range(len(retval)):
        column = retval[i]
        common_value = most_common(column)
        retval = retval[:,np.where(retval[i] == (not common - common_value))[0]]
        if retval.shape[1] == 1:
            return bits_to_int(retval[:,0])
    return None


@aoc.register(__file__)
def answers():
    data = np.array(aoc.read_grid(), dtype=int).T

    gamma = np.array([most_common(column) for column in data])
    epsilon = 1 - gamma
    yield bits_to_int(gamma) * bits_to_int(epsilon)

    oxygen = reduce_data(data)
    co2 = reduce_data(data, common=False)
    yield oxygen * co2

if __name__ == '__main__':
    aoc.run()
