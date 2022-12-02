import aoc
import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import convolve

    
def step(energy: NDArray) -> int:
    energy += 1
    flash_count = 0
    kernel = np.array([[1,1,1],[1,0,1],[1,1,1]])

    while ((energy > 9).sum() > 0):
        flashes = energy > 9
        neighbors = convolve(np.where(flashes, 1, 0), kernel, mode='constant')
        energy[flashes] = -99
        flash_count += np.sum(flashes)
        energy += neighbors
    energy[energy < 0] = 0
    return flash_count


@aoc.register(__file__)
def answers():
    energy_levels = np.array(aoc.read_grid(), dtype=int)

    flash_count = sum([step(energy_levels) for _ in range(100)])
    yield flash_count

    i = 100
    while np.any(energy_levels):
        step(energy_levels)
        i += 1
    yield i

if __name__ == '__main__':
    aoc.run()
