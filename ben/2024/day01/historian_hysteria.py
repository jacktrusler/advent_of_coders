import aoc
from collections import Counter


@aoc.register(__file__)
def answers():
    lists = list(zip(*[list(map(int, x.split())) for x in aoc.read_lines()]))

    # Part One
    columns = map(sorted, lists)
    yield sum([abs(x - y) for x, y in zip(*columns)])

    # Part Two
    left, right = [Counter(x) for x in lists]
    yield sum(k * v * right[k] for k, v in left.items())

if __name__ == '__main__':
    aoc.run()
