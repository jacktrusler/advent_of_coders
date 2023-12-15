import aoc
import numpy as np


def find_reflection(pattern: str, smudge: bool = False) -> int:
    ar = np.array(list(map(list, pattern.splitlines())))

    def _check_axis(axis: int) -> int:
        _ar = ar if axis == 0 else ar.T
        for i in range(1, len(_ar)):
            first, second = _ar[:i], _ar[i:]
            first = np.flip(first, axis=0)
            _len = min(len(first), len(second))
            first, second = first[:_len], second[:_len]
            _eq = first == second
            
            if (not smudge and np.all(_eq)) or \
               (smudge and np.count_nonzero(~_eq) == 1):
                return i
        return None
    
    if (row := _check_axis(0)):
        return 100 * row
    if (col := _check_axis(1)):
        return col
    return 0


@aoc.register(__file__)
def answers():
    patterns = aoc.read_chunks()
    yield sum(find_reflection(x) for x in patterns)
    yield sum(find_reflection(x, smudge=True) for x in patterns)

if __name__ == '__main__':
    aoc.run()
