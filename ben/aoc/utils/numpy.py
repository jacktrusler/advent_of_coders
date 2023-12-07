import numpy as np
from numpy.typing import NDArray
from scipy.ndimage import convolve
from typing import Any


ALL_ADJACENT = np.array([
    [1,1,1],
    [1,0,1],
    [1,1,1]
])
def count_adjacent(ar: NDArray, window=ALL_ADJACENT) -> NDArray:
    return convolve(ar, window, mode='constant')
