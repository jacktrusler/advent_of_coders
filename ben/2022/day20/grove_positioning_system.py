import aoc
import numpy as np
from numpy.typing import NDArray


def mix(nums: NDArray, num_times: int) -> int:
    nums = nums.copy()
    l = len(nums)

    for _ in range(num_times):
        for old_i in range(l):
            value, current_i = nums[old_i]
            new_i = (value + current_i) % (l - 1)
            if new_i > current_i:
                nums[:,1] = np.where(np.logical_and(nums[:,1] <= new_i, nums[:,1] > current_i), nums[:,1] - 1, nums[:,1])
            elif new_i < current_i:
                nums[:,1] = np.where(np.logical_and(nums[:,1] >= new_i, nums[:,1] < current_i), nums[:,1] + 1, nums[:,1])
            nums[old_i] = value, new_i

    zero_idx = nums[:,1][np.where(nums[:,0] == 0)[0][0]]
    indices = ((zero_idx + x) % l for x in (1000, 2000, 3000))
    vals = (nums[:,0][np.where(nums[:,1] == idx)[0][0]] for idx in indices)
    return sum(vals)


@aoc.register(__file__)
def answers():
    nums = np.array([(int(n), i) for i, n in enumerate(aoc.read_lines('data'))], dtype=np.int64)
    yield mix(nums, num_times=1)

    nums[:,0] *= 811_589_153
    yield mix(nums, num_times=10)

if __name__ == '__main__':
    aoc.run()
